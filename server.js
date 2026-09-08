import express from 'express';
import sqlite3 from 'sqlite3';
import cors from 'cors';
import bodyParser from 'body-parser';
import session from 'express-session';
import bcrypt from 'bcryptjs';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({ origin: true, credentials: true }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
  secret: process.env.SESSION_SECRET || 'salt-smoke-dev-secret',
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24 * 7 // 7 days
  }
}));

// Database setup
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const dbPath = path.join(__dirname, 'database.db');

// Serve the custom HTML, CSS, and JavaScript frontend from the same origin as the API.
app.use(express.static(__dirname));

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Connected to SQLite database');
    initializeDatabase();
  }
});

// Initialize database tables
function initializeDatabase() {
  db.serialize(() => {
    // Reservations table
    db.run(`
      CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        guests INTEGER NOT NULL,
        requests TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'confirmed'
      )
    `);

    db.run(`
      CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    db.all(`PRAGMA table_info(reservations)`, (err, columns) => {
      if (err) {
        console.error('Database schema check error:', err);
        return;
      }
      if (!columns.some(column => column.name === 'customer_id')) {
        db.run(
          `ALTER TABLE reservations ADD COLUMN customer_id INTEGER REFERENCES customers(id)`,
          alterErr => {
            if (alterErr) console.error('Database migration error:', alterErr);
          }
        );
      }
    });

    db.all(`PRAGMA table_info(customers)`, (err, columns) => {
      if (err) {
        console.error('Database schema check error:', err);
        return;
      }
      if (!columns.some(column => column.name === 'password_hash')) {
        db.run(
          `ALTER TABLE customers ADD COLUMN password_hash TEXT`,
          alterErr => {
            if (alterErr) console.error('Database migration error:', alterErr);
          }
        );
      }
    });

    // Newsletter signups table
    db.run(`
      CREATE TABLE IF NOT EXISTS newsletter_signups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'subscribed'
      )
    `);

    // Menu items table
    db.run(`
      CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        price REAL,
        image TEXT,
        is_chefs_pick INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    console.log('Database tables initialized');
  });
}

// Helper functions for validation
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateReservation(data) {
  const errors = [];
  
  if (!data.name || data.name.trim().length < 2) {
    errors.push('Name must be at least 2 characters');
  }
  if (!validateEmail(data.email)) {
    errors.push('Invalid email format');
  }
  if (!data.date) {
    errors.push('Date is required');
  }
  if (!data.time) {
    errors.push('Time is required');
  }
  if (!data.guests || data.guests < 1 || data.guests > 20) {
    errors.push('Guests must be between 1 and 20');
  }
  
  return errors;
}

function validateSignup(data) {
  const errors = [];

  if (!data.name || data.name.trim().length < 2) {
    errors.push('Name must be at least 2 characters');
  }
  if (!validateEmail(data.email)) {
    errors.push('Invalid email format');
  }
  if (!data.password || data.password.length < 6) {
    errors.push('Password must be at least 6 characters');
  }

  return errors;
}

// Requires an authenticated customer session; used to protect account-scoped routes.
function requireAuth(req, res, next) {
  if (!req.session || !req.session.customerId) {
    return res.status(401).json({ success: false, message: 'You must be logged in to do that' });
  }
  next();
}

// Routes

// Auth
app.post('/api/auth/signup', (req, res) => {
  const { name, email, password } = req.body;

  const validationErrors = validateSignup({ name, email, password });
  if (validationErrors.length > 0) {
    return res.status(400).json({ success: false, errors: validationErrors });
  }

  const normalizedEmail = email.trim().toLowerCase();

  db.get(`SELECT id FROM customers WHERE email = ?`, [normalizedEmail], (lookupErr, existing) => {
    if (lookupErr) {
      console.error('Database error:', lookupErr);
      return res.status(500).json({ success: false, message: 'Failed to check existing account' });
    }
    if (existing) {
      return res.status(400).json({ success: false, message: 'An account with that email already exists' });
    }

    const passwordHash = bcrypt.hashSync(password, 10);
    db.run(
      `INSERT INTO customers (name, email, password_hash) VALUES (?, ?, ?)`,
      [name.trim(), normalizedEmail, passwordHash],
      function(insertErr) {
        if (insertErr) {
          console.error('Database error:', insertErr);
          return res.status(500).json({ success: false, message: 'Failed to create account' });
        }
        req.session.customerId = this.lastID;
        req.session.customerName = name.trim();
        req.session.customerEmail = normalizedEmail;
        res.status(201).json({
          success: true,
          message: 'Account created successfully',
          customer: { id: this.lastID, name: name.trim(), email: normalizedEmail }
        });
      }
    );
  });
});

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;

  if (!validateEmail(email) || !password) {
    return res.status(400).json({ success: false, message: 'Email and password are required' });
  }

  const normalizedEmail = email.trim().toLowerCase();

  db.get(`SELECT * FROM customers WHERE email = ?`, [normalizedEmail], (err, customer) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ success: false, message: 'Failed to log in' });
    }
    if (!customer || !customer.password_hash || !bcrypt.compareSync(password, customer.password_hash)) {
      return res.status(401).json({ success: false, message: 'Invalid email or password' });
    }

    req.session.customerId = customer.id;
    req.session.customerName = customer.name;
    req.session.customerEmail = customer.email;
    res.json({
      success: true,
      message: 'Logged in successfully',
      customer: { id: customer.id, name: customer.name, email: customer.email }
    });
  });
});

app.post('/api/auth/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Session destroy error:', err);
      return res.status(500).json({ success: false, message: 'Failed to log out' });
    }
    res.clearCookie('connect.sid');
    res.json({ success: true, message: 'Logged out successfully' });
  });
});

app.get('/api/auth/me', (req, res) => {
  if (!req.session || !req.session.customerId) {
    return res.json({ success: true, customer: null });
  }
  res.json({
    success: true,
    customer: {
      id: req.session.customerId,
      name: req.session.customerName,
      email: req.session.customerEmail
    }
  });
});

// Reservations tied to the logged-in customer's account
app.get('/api/my/reservations', requireAuth, (req, res) => {
  db.all(
    `SELECT * FROM reservations WHERE customer_id = ? ORDER BY date DESC, time DESC`,
    [req.session.customerId],
    (err, rows) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ success: false, message: 'Failed to fetch your reservations' });
      }
      res.json({ success: true, data: rows });
    }
  );
});

app.post('/api/my/reservations', requireAuth, (req, res) => {
  const { date, time = '19:30', guests, requests } = req.body;
  const name = req.session.customerName;
  const email = req.session.customerEmail;

  const validationErrors = validateReservation({ name, email, date, time, guests });
  if (validationErrors.length > 0) {
    return res.status(400).json({ success: false, errors: validationErrors });
  }

  db.run(
    `INSERT INTO reservations (name, email, date, time, guests, requests, customer_id)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [name, email, date, time, guests, requests || '', req.session.customerId],
    function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ success: false, message: 'Failed to create reservation' });
      }
      res.status(201).json({
        success: true,
        message: 'Reservation created successfully',
        reservationId: this.lastID
      });
    }
  );
});

app.delete('/api/my/reservations/:id', requireAuth, (req, res) => {
  db.get(
    `SELECT * FROM reservations WHERE id = ? AND customer_id = ?`,
    [req.params.id, req.session.customerId],
    (err, reservation) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ success: false, message: 'Failed to cancel reservation' });
      }
      if (!reservation) {
        return res.status(404).json({ success: false, message: 'Reservation not found' });
      }
      if (reservation.status === 'cancelled') {
        return res.status(409).json({ success: false, message: 'Reservation is already cancelled' });
      }
      db.run(
        `UPDATE reservations SET status = 'cancelled' WHERE id = ? AND customer_id = ?`,
        [req.params.id, req.session.customerId],
        function(updateErr) {
          if (updateErr) {
            console.error('Database error:', updateErr);
            return res.status(500).json({ success: false, message: 'Failed to cancel reservation' });
          }
          res.json({
            success: true,
            message: 'Reservation cancelled successfully',
            data: { ...reservation, status: 'cancelled' }
          });
        }
      );
    }
  );
});

// Reservations
app.post('/api/reservations', (req, res) => {
  const { name, email, date, time = '19:30', guests, requests } = req.body;
  
  const validationErrors = validateReservation({ name, email, date, time, guests });
  if (validationErrors.length > 0) {
    return res.status(400).json({ 
      success: false, 
      errors: validationErrors 
    });
  }

  db.run(`INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)`, [name.trim(), email.trim()], customerErr => {
    if (customerErr) {
      console.error('Database error:', customerErr);
      return res.status(500).json({ success: false, message: 'Failed to save customer details' });
    }
    db.get(`SELECT id FROM customers WHERE email = ?`, [email.trim()], (lookupErr, customer) => {
      if (lookupErr || !customer) {
        console.error('Database error:', lookupErr);
        return res.status(500).json({ success: false, message: 'Failed to link reservation to customer' });
      }
      db.run(
        `INSERT INTO reservations (name, email, date, time, guests, requests, customer_id)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [name.trim(), email.trim(), date, time, guests, requests || '', customer.id],
        function(err) {
          if (err) {
            console.error('Database error:', err);
            return res.status(500).json({ success: false, message: 'Failed to create reservation' });
          }
          res.status(201).json({
            success: true,
            message: 'Reservation created successfully',
            reservationId: this.lastID
          });
        }
      );
    });
  });
});

app.get('/api/reservations', (req, res) => {
  db.all(
    `SELECT * FROM reservations ORDER BY date DESC, time DESC`,
    (err, rows) => {
      if (err) {
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to fetch reservations' 
        });
      }
      res.json({ success: true, data: rows });
    }
  );
});

app.get('/api/reservations/:id', (req, res) => {
  db.get(
    `SELECT * FROM reservations WHERE id = ?`,
    [req.params.id],
    (err, row) => {
      if (err) {
        return res.status(500).json({
          success: false,
          message: 'Failed to fetch reservation'
        });
      }
      if (!row) {
        return res.status(404).json({
          success: false,
          message: 'Reservation not found'
        });
      }
      res.json({ success: true, data: row });
    }
  );
});

app.put('/api/reservations/:id', (req, res) => {
  const { name, email, date, time = '19:30', guests, requests, status } = req.body;
  const validationErrors = validateReservation({ name, email, date, time, guests });
  if (validationErrors.length > 0) {
    return res.status(400).json({ success: false, errors: validationErrors });
  }

  db.run(
    `UPDATE reservations
     SET name = ?, email = ?, date = ?, time = ?, guests = ?, requests = ?, status = ?
     WHERE id = ?`,
    [name.trim(), email.trim(), date, time, guests, requests || '', status || 'confirmed', req.params.id],
    function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ success: false, message: 'Failed to update reservation' });
      }
      if (this.changes === 0) {
        return res.status(404).json({ success: false, message: 'Reservation not found' });
      }
      res.json({ success: true, message: 'Reservation updated successfully' });
    }
  );
});

app.delete('/api/reservations/:id', (req, res) => {
  db.run(`DELETE FROM reservations WHERE id = ?`, [req.params.id], function(err) {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ success: false, message: 'Failed to delete reservation' });
    }
    if (this.changes === 0) {
      return res.status(404).json({ success: false, message: 'Reservation not found' });
    }
    res.json({ success: true, message: 'Reservation deleted successfully' });
  });
});

// Newsletter
app.post('/api/newsletter/signup', (req, res) => {
  const { email } = req.body;
  
  if (!validateEmail(email)) {
    return res.status(400).json({ 
      success: false, 
      message: 'Invalid email format' 
    });
  }

  db.run(
    `INSERT INTO newsletter_signups (email) VALUES (?)`,
    [email],
    function(err) {
      if (err) {
        if (err.message.includes('UNIQUE constraint failed')) {
          return res.status(400).json({ 
            success: false, 
            message: 'Email already subscribed' 
          });
        }
        console.error('Database error:', err);
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to subscribe' 
        });
      }
      res.status(201).json({ 
        success: true, 
        message: 'Successfully subscribed to newsletter',
        signupId: this.lastID
      });
    }
  );
});

app.get('/api/newsletter/signups', (req, res) => {
  db.all(
    `SELECT * FROM newsletter_signups ORDER BY created_at DESC`,
    (err, rows) => {
      if (err) {
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to fetch signups' 
        });
      }
      res.json({ success: true, data: rows });
    }
  );
});

// Menu
app.post('/api/menu', (req, res) => {
  const { name, category, description, price, image, is_chefs_pick } = req.body;
  
  if (!name || !category) {
    return res.status(400).json({ 
      success: false, 
      message: 'Name and category are required' 
    });
  }

  db.run(
    `INSERT INTO menu_items (name, category, description, price, image, is_chefs_pick) 
     VALUES (?, ?, ?, ?, ?, ?)`,
    [name, category, description || '', price || 0, image || '', is_chefs_pick ? 1 : 0],
    function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to create menu item' 
        });
      }
      res.status(201).json({ 
        success: true, 
        message: 'Menu item created successfully',
        menuId: this.lastID
      });
    }
  );
});

app.get('/api/menu', (req, res) => {
  const { category } = req.query;
  
  let query = 'SELECT * FROM menu_items';
  const params = [];
  
  if (category) {
    query += ' WHERE category = ?';
    params.push(category);
  }
  
  query += ' ORDER BY is_chefs_pick DESC, name ASC';
  
  db.all(query, params, (err, rows) => {
    if (err) {
      return res.status(500).json({ 
        success: false, 
        message: 'Failed to fetch menu' 
      });
    }
    res.json({ success: true, data: rows });
  });
});

app.get('/api/menu/:id', (req, res) => {
  db.get(
    `SELECT * FROM menu_items WHERE id = ?`,
    [req.params.id],
    (err, row) => {
      if (err) {
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to fetch menu item' 
        });
      }
      if (!row) {
        return res.status(404).json({ 
          success: false, 
          message: 'Menu item not found' 
        });
      }
      res.json({ success: true, data: row });
    }
  );
});

app.put('/api/menu/:id', (req, res) => {
  const { name, category, description, price, image, is_chefs_pick } = req.body;
  
  db.run(
    `UPDATE menu_items SET name = ?, category = ?, description = ?, price = ?, image = ?, is_chefs_pick = ? 
     WHERE id = ?`,
    [name, category, description || '', price || 0, image || '', is_chefs_pick ? 1 : 0, req.params.id],
    function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to update menu item' 
        });
      }
      if (this.changes === 0) {
        return res.status(404).json({ 
          success: false, 
          message: 'Menu item not found' 
        });
      }
      res.json({ 
        success: true, 
        message: 'Menu item updated successfully' 
      });
    }
  );
});

app.delete('/api/menu/:id', (req, res) => {
  db.run(
    `DELETE FROM menu_items WHERE id = ?`,
    [req.params.id],
    function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ 
          success: false, 
          message: 'Failed to delete menu item' 
        });
      }
      if (this.changes === 0) {
        return res.status(404).json({ 
          success: false, 
          message: 'Menu item not found' 
        });
      }
      res.json({ 
        success: true, 
        message: 'Menu item deleted successfully' 
      });
    }
  );
});

app.get('/api/docs', (req, res) => {
  res.sendFile(path.join(__dirname, 'API-DOCUMENTATION.md'));
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'API is running' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🍽️  Salt & Smoke API running on http://localhost:${PORT}`);
  console.log(`📚 API Documentation available at http://localhost:${PORT}/api/docs`);
});

export default app;
