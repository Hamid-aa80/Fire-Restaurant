# Fire_Restaurant API Documentation

## Overview

The Fire_Restaurant API is a backend service for managing reservations, newsletter signups, and menu items for the Fire_Restaurant restaurant.

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Create and activate a virtual environment, then install Python requirements:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Apply database migrations and start Django:
```bash
python manage.py migrate --fake-initial
python manage.py runserver 0.0.0.0:5000
```

The API will be available at `http://localhost:5000`

### Authentication

Create a staff account with `python manage.py createsuperuser` and sign in at
`/admin/`. Django sessions authenticate the protected API endpoints. Reservation
and table availability features require a customer account. Customers register
at `/accounts/register/` and log in at `/accounts/login/`; these pages create
Django-authenticated sessions. Customers may view, create, update, and delete
only their own bookings. Staff can manage all bookings through the admin site.
Newsletter signup and menu reads do not require an account.

## API Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "API is running"
}
```

---

## Reservations

### Create Reservation

**POST** `/api/reservations`

Create a reservation for the authenticated customer and a currently available
table. A customer can book one table for 1–4 guests. A `table` ID can be
obtained from the availability endpoint.

**Request Body:**
```json
{
  "table": 1,
  "date": "2027-12-25",
  "time": "19:30",
  "guests": 4,
  "requests": "Window seat, celebration for anniversary"
}
```

**GET** `/api/reservations/availability?date=2027-12-25&time=19:30&guests=4`

Returns the configured tables and whether each can accommodate the selected
party at that date and time. Login is required.

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Reservation created successfully",
  "reservationId": 1
}
```

**Response (Error - 400/401/409):**
```json
{
  "success": false,
  "errors": ["That table is already booked at this date and time."]
}
```

**Validation Rules:**
- `table`: Required, available table ID with enough seats
- `date`: Required, ISO date format (YYYY-MM-DD)
- `time`: Required, HH:MM format
- `guests`: Required, integer between 1 and 4
- `requests`: Optional, special dining requests
- Past dates/times, occupied table slots, and repeat bookings by the same customer for the same slot are rejected.

---

### Get All Reservations

**GET** `/api/reservations`

Retrieve all reservations belonging to the authenticated customer. Staff users
can retrieve all reservations.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "customerId": 1,
      "tableId": 1,
      "tableNumber": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "date": "2024-12-25",
      "time": "19:30",
      "guests": 4,
      "requests": "Window seat, celebration for anniversary",
      "created_at": "2024-12-01T10:30:00Z",
      "status": "confirmed"
    }
  ]
}
```

---

### Get Reservation by ID

**GET** `/api/reservations/:id`

Retrieve, update, or delete a reservation belonging to the authenticated
customer. Staff users may manage all reservations. Update requests use `PUT`
with `table`, `date`, `time`, `guests`, and optional `requests`.

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "customerId": 1,
    "tableId": 1,
    "tableNumber": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-12-25",
    "time": "19:30",
    "guests": 4,
    "requests": "Window seat",
    "created_at": "2024-12-01T10:30:00Z",
    "status": "confirmed"
  }
}
```

**Response (Error - 404):**
```json
{
  "success": false,
  "message": "Reservation not found"
}
```

---

## Newsletter

### Subscribe to Newsletter

**POST** `/api/newsletter/signup`

Subscribe an email address to the newsletter.

**Request Body:**
```json
{
  "email": "subscriber@example.com"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Successfully subscribed to newsletter",
  "signupId": 1
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Email already subscribed"
}
```

**Validation Rules:**
- `email`: Required, valid email format, must be unique

---

### Get Newsletter Signups

**GET** `/api/newsletter/signups`

Retrieve all newsletter subscribers (staff authentication required).

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "email": "subscriber@example.com",
      "created_at": "2024-12-01T10:30:00Z",
      "status": "subscribed"
    }
  ]
}
```

---

## Menu

### Get All Menu Items

**GET** `/api/menu`

Retrieve all menu items, optionally filtered by category.

**Query Parameters:**
- `category` (optional): Filter by category (e.g., "breakfast", "lunch", "dinner", "drinks")

**Examples:**
- `/api/menu` - Get all items
- `/api/menu?category=lunch` - Get lunch items only

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Smoked Brisket",
      "category": "lunch",
      "description": "Slow-smoked Texas-style brisket",
      "price": 24.99,
      "image": "https://example.com/brisket.jpg",
      "is_chefs_pick": 1,
      "created_at": "2024-12-01T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Pulled Pork Sandwich",
      "category": "lunch",
      "description": "Tender pulled pork with house BBQ sauce",
      "price": 15.99,
      "image": "https://example.com/pork.jpg",
      "is_chefs_pick": 0,
      "created_at": "2024-12-01T10:30:00Z"
    }
  ]
}
```

---

### Get Menu Item by ID

**GET** `/api/menu/:id`

Retrieve a specific menu item. This endpoint is public.

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Smoked Brisket",
    "category": "lunch",
    "description": "Slow-smoked Texas-style brisket",
    "price": 24.99,
    "image": "https://example.com/brisket.jpg",
    "is_chefs_pick": 1,
    "created_at": "2024-12-01T10:30:00Z"
  }
}
```

**Response (Error - 404):**
```json
{
  "success": false,
  "message": "Menu item not found"
}
```

---

### Create Menu Item

**POST** `/api/menu`

Create a new menu item (staff authentication required).

**Request Body:**
```json
{
  "name": "Smoked Brisket",
  "category": "lunch",
  "description": "Slow-smoked Texas-style brisket",
  "price": 24.99,
  "image": "https://example.com/brisket.jpg",
  "is_chefs_pick": true
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Menu item created successfully",
  "menuId": 1
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "errors": ["This field is required."]
}
```

**Required Fields:**
- `name`: Menu item name
- `category`: Category (breakfast, lunch, dinner, drinks, etc.)

**Optional Fields:**
- `description`: Item description
- `price`: Item price (default: 0)
- `image`: Image URL
- `is_chefs_pick`: Boolean, marks as chef's special (default: false)

---

### Update Menu Item

**PUT** `/api/menu/:id`

Update an existing menu item (staff authentication required).

**Request Body:**
```json
{
  "name": "Smoked Brisket",
  "category": "lunch",
  "description": "Updated description",
  "price": 25.99,
  "image": "https://example.com/brisket-new.jpg",
  "is_chefs_pick": false
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Menu item updated successfully"
}
```

---

### Delete Menu Item

**DELETE** `/api/menu/:id`

Delete a menu item (staff authentication required).

**Response (Success):**
```json
{
  "success": true,
  "message": "Menu item deleted successfully"
}
```

**Response (Error - 404):**
```json
{
  "success": false,
  "message": "Menu item not found"
}
```

---

## Error Handling

All endpoints return standardized error responses:

**HTTP Status Codes:**
- `200` - OK
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Authentication required
- `403` - Staff access required
- `404` - Not Found
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "success": false,
  "message": "Error description",
  "errors": ["Specific error 1", "Specific error 2"]
}
```

---

## Authentication and CSRF

Staff API requests use the authenticated Django admin session. Django CSRF
protection applies to menu changes; send a valid CSRF token with those requests.
The browser-based admin interface at `/admin/` includes the required protection.
Reservation create/update/delete requests also require an authenticated
customer session and a valid CSRF token when submitted through a browser.

---

## Database

The Django ORM manages `Customer`, `Reservation`, `MenuItem`, and
`NewsletterSignup` models and the `RestaurantTable` inventory. Every
reservation references one customer and one four-seat table through foreign
keys. Database unique constraints prevent duplicate customer/date/time and
table/date/time entries. The migration seeds 20 tables and assigns existing
reservations without deleting booking records.

The API uses SQLite with the following tables:

### Reservations Table
- `id` - Auto-increment ID
- `name` - Customer name
- `email` - Customer email
- `date` - Reservation date
- `time` - Reservation time
- `guests` - Number of guests
- `requests` - Special requests
- `created_at` - Timestamp
- `status` - Reservation status (confirmed)

### Newsletter Signups Table
- `id` - Auto-increment ID
- `email` - Subscriber email (unique)
- `created_at` - Timestamp
- `status` - Subscription status (subscribed)

### Menu Items Table
- `id` - Auto-increment ID
- `name` - Item name
- `category` - Item category
- `description` - Item description
- `price` - Item price
- `image` - Image URL
- `is_chefs_pick` - Boolean flag
- `created_at` - Timestamp

---

## Frontend Integration

Use the provided `api-client.js` to integrate the API with your frontend:

```javascript
import { reservationsAPI, newsletterAPI, menuAPI } from './api-client.js';

// Create a reservation
const result = await reservationsAPI.create({
  name: 'John Doe',
  email: 'john@example.com',
  date: '2024-12-25',
  time: '19:30',
  guests: 4,
  requests: 'Window seat'
});

// Get all menu items
const menu = await menuAPI.getAll();

// Get lunch items
const lunch = await menuAPI.getAll('lunch');

// Subscribe to newsletter
const signup = await newsletterAPI.signup('subscriber@example.com');
```

---

## Development

### Running the Server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --fake-initial
python manage.py runserver 0.0.0.0:5000
```

Create a staff login for the admin site and protected endpoints:

```bash
python manage.py createsuperuser
```

### Database

The Django models use SQLite at `database.db` by default. The initial migration
reuses the existing reservation, newsletter, and menu tables. A new database
will receive those tables through the same migration command.

Set `DATABASE_NAME` to use a different database file.

---

## Future Enhancements

- Email notifications for reservations
- Payment processing
- Review & ratings system
- Inventory management
- Order history tracking
- Admin dashboard
