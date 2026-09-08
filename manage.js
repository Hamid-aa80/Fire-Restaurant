const form = document.querySelector("#menuForm");
const list = document.querySelector("#menuList");
const feedback = document.querySelector("#manageFeedback");
let items = [];

const showFeedback = (message, type = "success") => {
  feedback.className = `alert alert-${type}`;
  feedback.textContent = message;
};

const clearForm = () => {
  form.reset();
  document.querySelector("#itemId").value = "";
};

const fillForm = item => {
  document.querySelector("#itemId").value = item.id;
  document.querySelector("#itemName").value = item.name;
  document.querySelector("#itemCategory").value = item.category;
  document.querySelector("#itemDescription").value = item.description || "";
  document.querySelector("#itemPrice").value = item.price ?? 0;
  document.querySelector("#itemChefPick").checked = Boolean(item.is_chefs_pick);
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const render = () => {
  const term = document.querySelector("#searchItems").value.trim().toLowerCase();
  const visible = items.filter(item =>
    `${item.name} ${item.category}`.toLowerCase().includes(term)
  );
  list.textContent = "";
  if (!visible.length) {
    list.innerHTML = '<p class="text-muted mb-0">No menu records found.</p>';
    return;
  }
  visible.forEach(item => {
    const row = document.createElement("div");
    row.className = "list-group-item d-flex justify-content-between gap-3 align-items-start";
    row.innerHTML = `
      <div>
        <strong>${item.name}</strong>
        <span class="badge text-bg-secondary ms-2">${item.category}</span>
        <p class="small text-muted mb-0">${item.description || "No description"}</p>
        <span class="small">£${Number(item.price || 0).toFixed(2)}</span>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-sm btn-outline-primary edit-item" type="button">Edit</button>
        <button class="btn btn-sm btn-outline-danger delete-item" type="button">Delete</button>
      </div>`;
    row.querySelector(".edit-item").addEventListener("click", () => fillForm(item));
    row.querySelector(".delete-item").addEventListener("click", async () => {
      if (!window.confirm(`Delete ${item.name}?`)) return;
      const response = await fetch(`/api/menu/${item.id}`, { method: "DELETE" });
      if (!response.ok) throw new Error("Menu record could not be deleted.");
      items = items.filter(candidate => candidate.id !== item.id);
      render();
      showFeedback("Menu record deleted.");
    });
    list.appendChild(row);
  });
};

const loadItems = async () => {
  const response = await fetch("/api/menu");
  if (!response.ok) throw new Error("Menu records could not be loaded.");
  const result = await response.json();
  items = result.data;
  render();
};

form.addEventListener("submit", async event => {
  event.preventDefault();
  const id = document.querySelector("#itemId").value;
  const payload = {
    name: document.querySelector("#itemName").value.trim(),
    category: document.querySelector("#itemCategory").value.trim(),
    description: document.querySelector("#itemDescription").value.trim(),
    price: Number(document.querySelector("#itemPrice").value),
    is_chefs_pick: document.querySelector("#itemChefPick").checked
  };
  try {
    const response = await fetch(id ? `/api/menu/${id}` : "/api/menu", {
      method: id ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Menu record could not be saved.");
    clearForm();
    await loadItems();
    showFeedback(id ? "Menu record updated." : "Menu record created.");
  } catch (error) {
    showFeedback(error.message, "danger");
  }
});

document.querySelector("#newItemButton").addEventListener("click", clearForm);
document.querySelector("#cancelButton").addEventListener("click", clearForm);
document.querySelector("#searchItems").addEventListener("input", render);

loadItems().catch(error => showFeedback(`${error.message} Start the app with npm start.`, "danger"));
