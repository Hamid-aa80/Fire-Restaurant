// account.js — Salt & Smoke customer sign up, login, and reservation management

document.addEventListener("DOMContentLoaded", () => {
  const authFeedback = document.getElementById("authFeedback");
  const authForms = document.getElementById("authForms");
  const accountDashboard = document.getElementById("accountDashboard");
  const accountGreeting = document.getElementById("accountGreeting");

  const signupForm = document.getElementById("signupForm");
  const loginForm = document.getElementById("loginForm");
  const logoutButton = document.getElementById("logoutButton");

  const myReservationForm = document.getElementById("myReservationForm");
  const myReservationsList = document.getElementById("myReservationsList");
  const dateInput = document.getElementById("myReservationDate");

  const today = new Date().toISOString().split("T")[0];
  if (dateInput) dateInput.min = today;

  const showFeedback = (message, type = "danger") => {
    if (!authFeedback) return;
    authFeedback.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning", "alert-info");
    authFeedback.classList.add("alert", `alert-${type}`);
    authFeedback.textContent = message;
  };

  const hideFeedback = () => {
    if (!authFeedback) return;
    authFeedback.classList.add("d-none");
    authFeedback.textContent = "";
  };

  const showLoggedInView = customer => {
    if (authForms) authForms.classList.add("d-none");
    if (accountDashboard) accountDashboard.classList.remove("d-none");
    if (accountGreeting) accountGreeting.textContent = `Hello, ${customer.name}!`;
  };

  const showLoggedOutView = () => {
    if (authForms) authForms.classList.remove("d-none");
    if (accountDashboard) accountDashboard.classList.add("d-none");
  };

  const renderReservations = reservations => {
    if (!myReservationsList) return;
    myReservationsList.textContent = "";

    if (!reservations.length) {
      myReservationsList.innerHTML = '<p class="text-muted mb-0">You have no reservations yet.</p>';
      return;
    }

    reservations.forEach(reservation => {
      const item = document.createElement("div");
      item.className = "d-flex justify-content-between align-items-start gap-3 border-bottom py-3";
      const formattedDate = new Date(`${reservation.date}T00:00:00`).toLocaleDateString("en-GB", {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric"
      });
      const isCancelled = reservation.status === "cancelled";
      item.innerHTML = `
        <div>
          <strong>${formattedDate}</strong> at ${reservation.time}
          <span class="badge text-bg-secondary ms-2">${reservation.guests} guest${reservation.guests === 1 ? "" : "s"}</span>
          <span class="badge text-bg-info ms-1">${reservation.status}</span>
          ${reservation.requests ? `<p class="small text-muted mb-0 mt-1">${reservation.requests}</p>` : ""}
        </div>
        ${isCancelled
          ? '<span class="small text-muted">Cancelled</span>'
          : '<button class="btn btn-sm btn-outline-danger cancel-reservation" type="button">Cancel</button>'}
      `;
      const cancelButton = item.querySelector(".cancel-reservation");
      if (!cancelButton) {
        myReservationsList.appendChild(item);
        return;
      }
      cancelButton.addEventListener("click", async () => {
        if (!window.confirm("Cancel this reservation?")) return;
        cancelButton.disabled = true;
        try {
          const response = await fetch(`/api/my/reservations/${reservation.id}`, {
            method: "DELETE",
            credentials: "include"
          });
          const result = await response.json();
          if (!response.ok || !result.success) {
            throw new Error(result.message || "Reservation could not be cancelled.");
          }
          showFeedback("Reservation cancelled successfully.", "success");
          await loadMyReservations();
        } catch (error) {
          showFeedback(error.message, "danger");
          cancelButton.disabled = false;
        }
      });
      myReservationsList.appendChild(item);
    });
  };

  const loadMyReservations = async () => {
    try {
      const response = await fetch("/api/my/reservations", { credentials: "include" });
      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.message || "Could not load your reservations.");
      }
      renderReservations(result.data);
    } catch (error) {
      showFeedback(error.message, "danger");
    }
  };

  const checkSession = async () => {
    try {
      const response = await fetch("/api/auth/me", { credentials: "include" });
      const result = await response.json();
      if (result.success && result.customer) {
        showLoggedInView(result.customer);
        await loadMyReservations();
      } else {
        showLoggedOutView();
      }
    } catch (error) {
      showLoggedOutView();
    }
  };

  if (signupForm) {
    signupForm.addEventListener("submit", async event => {
      event.preventDefault();
      hideFeedback();

      const name = document.getElementById("signupName").value.trim();
      const email = document.getElementById("signupEmail").value.trim();
      const password = document.getElementById("signupPassword").value;

      try {
        const response = await fetch("/api/auth/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ name, email, password })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.errors?.join(", ") || result.message || "Sign up failed.");
        }
        signupForm.reset();
        showFeedback("Account created successfully! You're now logged in.", "success");
        showLoggedInView(result.customer);
        await loadMyReservations();
      } catch (error) {
        showFeedback(error.message, "danger");
      }
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", async event => {
      event.preventDefault();
      hideFeedback();

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value;

      try {
        const response = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ email, password })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.message || "Login failed.");
        }
        loginForm.reset();
        showFeedback("Logged in successfully.", "success");
        showLoggedInView(result.customer);
        await loadMyReservations();
      } catch (error) {
        showFeedback(error.message, "danger");
      }
    });
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
      hideFeedback();
      try {
        const response = await fetch("/api/auth/logout", {
          method: "POST",
          credentials: "include"
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.message || "Logout failed.");
        }
        showFeedback("You have been logged out.", "success");
        showLoggedOutView();
      } catch (error) {
        showFeedback(error.message, "danger");
      }
    });
  }

  if (myReservationForm) {
    myReservationForm.addEventListener("submit", async event => {
      event.preventDefault();
      hideFeedback();

      const date = document.getElementById("myReservationDate").value;
      const time = document.getElementById("myReservationTime").value;
      const guests = Number(document.getElementById("myReservationGuests").value);
      const requests = document.getElementById("myReservationRequests").value.trim();

      try {
        const response = await fetch("/api/my/reservations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ date, time, guests, requests })
        });
        const result = await response.json();
        if (!response.ok || !result.success) {
          throw new Error(result.errors?.join(", ") || result.message || "Reservation could not be saved.");
        }
        myReservationForm.reset();
        showFeedback("Reservation booked successfully!", "success");
        await loadMyReservations();
      } catch (error) {
        showFeedback(error.message, "danger");
      }
    });
  }

  checkSession();
});
