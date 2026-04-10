const statusMessage = document.getElementById("status-message");
const results = document.getElementById("results");

const mockPets = [
  { pet_id: 1, name: "Milo", species: "Dog", age: 3, available: true },
  { pet_id: 2, name: "Luna", species: "Cat", age: 2, available: false },
  { pet_id: 3, name: "Coco", species: "Rabbit", age: 1, available: true }
];

const mockApplications = [
  {
    application_id: 101,
    user_id: 1,
    pet_id: 1,
    status: "Pending",
    submitted_at: "2026-04-10 10:00",
    notes: "Lives near a dog park"
  },
  {
    application_id: 102,
    user_id: 2,
    pet_id: 2,
    status: "Approved",
    submitted_at: "2026-04-09 14:30",
    notes: "Previous cat owner"
  }
];

const actions = {
  view_all_pets: () => {
    renderTable(mockPets, ["pet_id", "name", "species", "age", "available"]);
    setMessage("Previewing `view_all_pets()` with sample Pet rows.");
  },
  view_available_pets: () => {
    const availablePets = mockPets.filter((pet) => pet.available);
    renderTable(availablePets, ["pet_id", "name", "species", "age", "available"]);
    setMessage("Previewing `view_available_pets()` with available pets only.");
  },
  view_all_applications: () => {
    renderTable(mockApplications, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"]);
    setMessage("Previewing `view_all_applications()`.");
  },
  count_applications_per_pet: () => {
    const summary = mockPets.map((pet) => ({
      pet_id: pet.pet_id,
      pet_name: pet.name,
      application_count: mockApplications.filter((app) => app.pet_id === pet.pet_id).length
    }));
    renderTable(summary, ["pet_id", "pet_name", "application_count"]);
    setMessage("Previewing `count_applications_per_pet()`.");
  },
  view_approved_applications: () => {
    const approved = mockApplications.filter((app) => app.status === "Approved");
    renderTable(approved, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"]);
    setMessage("Previewing `view_approved_applications()`.");
  }
};

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    actions[action]?.();
  });
});

document.getElementById("submit-application-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData.entries());

  setMessage("Prototype only: this will later call the Python `submit_application()` logic.");
  results.innerHTML = `<pre>${JSON.stringify(payload, null, 2)}</pre>`;
});

document.getElementById("pet-search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const petId = Number(new FormData(event.target).get("pet_id"));
  const filtered = mockApplications.filter((app) => app.pet_id === petId);

  renderTable(filtered, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"]);
  setMessage(`Previewing \`view_applications_by_pet()\` for pet_id = ${petId}.`);
});

document.getElementById("user-search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const userId = Number(new FormData(event.target).get("user_id"));
  const filtered = mockApplications.filter((app) => app.user_id === userId);

  renderTable(filtered, ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"]);
  setMessage(`Previewing \`view_applications_by_user()\` for user_id = ${userId}.`);
});

document.getElementById("status-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = Object.fromEntries(new FormData(event.target).entries());

  setMessage("Prototype only: this will later call `update_application_status()` in the backend.");
  results.innerHTML = `<pre>${JSON.stringify(formData, null, 2)}</pre>`;
});

function setMessage(message) {
  statusMessage.textContent = `${message} Backend connection is not wired up yet.`;
}

function renderTable(rows, columns) {
  if (!rows.length) {
    results.innerHTML = '<p class="notice">No records found in this prototype view.</p>';
    return;
  }

  const headerRow = columns.map((column) => `<th>${column}</th>`).join("");
  const bodyRows = rows
    .map((row) => {
      const cells = columns.map((column) => `<td>${row[column] ?? ""}</td>`).join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  results.innerHTML = `
    <table>
      <thead>
        <tr>${headerRow}</tr>
      </thead>
      <tbody>
        ${bodyRows}
      </tbody>
    </table>
  `;
}

setMessage("Simple front end scaffold loaded.");
renderTable(mockPets, ["pet_id", "name", "species", "age", "available"]);
