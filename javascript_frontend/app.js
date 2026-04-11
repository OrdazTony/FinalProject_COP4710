const statusMessage = document.getElementById("status-message");
const results = document.getElementById("results");
const queryTitle = document.getElementById("query-title");
const queryPreview = document.getElementById("query-preview");
const userSelect = document.getElementById("user-select");
const petSelect = document.getElementById("pet-select");

const users = [
  { user_id: 1, name: "Alice Johnson", email: "alice@example.com" },
  { user_id: 2, name: "Brian Lee", email: "brian@example.com" },
  { user_id: 3, name: "Carla Mendes", email: "carla@example.com" },
  { user_id: 4, name: "David Smith", email: "david@example.com" }
];

const pets = [];

const fallbackPets = [
  { pet_id: 101, name: "Buddy", species: "Dog", age: 3, available: false },
  { pet_id: 102, name: "Mittens", species: "Cat", age: 2, available: true },
  { pet_id: 103, name: "Rocky", species: "Dog", age: 7, available: false },
  { pet_id: 104, name: "Coco", species: "Bird", age: 0, available: true },
  { pet_id: 105, name: "Luna", species: "Cat", age: 12, available: true }
];

const applications = [
  {
    application_id: 1,
    user_id: 1,
    pet_id: 101,
    status: "Pending",
    submitted_at: "2026-04-01 10:30:00",
    notes: "Looking for a family dog"
  },
  {
    application_id: 2,
    user_id: 2,
    pet_id: 102,
    status: "Approved",
    submitted_at: "2026-04-02 14:00:00",
    notes: "Has experience with cats"
  },
  {
    application_id: 3,
    user_id: 3,
    pet_id: 103,
    status: "Rejected",
    submitted_at: "2026-04-03 09:15:00",
    notes: null
  },
  {
    application_id: 4,
    user_id: 1,
    pet_id: 105,
    status: "Withdrawn",
    submitted_at: "2026-04-04 16:45:00",
    notes: "Moved to a smaller apartment"
  },
  {
    application_id: 5,
    user_id: 4,
    pet_id: 101,
    status: "Pending",
    submitted_at: "2026-04-05 11:20:00",
    notes: null
  }
];

const queryCatalog = {
  view_all_pets: {
    title: "Query 1 · View all pets",
    sql: `SELECT pet_id, name, species, age, available\nFROM Pet\nORDER BY pet_id;`
  },
  view_available_pets: {
    title: "Query 2 · View available pets",
    sql: `SELECT pet_id, name, species, age, available\nFROM Pet\nWHERE available = TRUE\nORDER BY pet_id;`
  },
  count_applications_per_pet: {
    title: "Query 3 · Count applications per pet",
    sql: `SELECT p.pet_id, p.name AS pet_name, COUNT(a.application_id) AS application_count\nFROM Pet p\nLEFT JOIN AdoptionApplication a ON p.pet_id = a.pet_id\nGROUP BY p.pet_id, p.name\nORDER BY p.pet_id;`
  },
  view_approved_applications: {
    title: "Query 4 · View approved applications",
    sql: `SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE status = 'Approved'\nORDER BY application_id;`
  },
  view_all_applications: {
    title: "Query 5 · View all applications",
    sql: `SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nORDER BY application_id;`
  },
  view_applications_by_pet: {
    title: "Query 6 · View applications by pet",
    sql: `SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE pet_id = 101\nORDER BY application_id;`
  },
  view_applications_by_user: {
    title: "Query 7 · View applications by user",
    sql: `SELECT application_id, user_id, pet_id, status, submitted_at, notes\nFROM AdoptionApplication\nWHERE user_id = 1\nORDER BY application_id;`
  },
  view_named_applications: {
    title: "Query 8 · Application details with names",
    sql: `SELECT a.application_id, u.name AS user_name, p.name AS pet_name, a.status, a.submitted_at, a.notes\nFROM AdoptionApplication a\nJOIN UserTable u ON a.user_id = u.user_id\nJOIN Pet p ON a.pet_id = p.pet_id\nORDER BY a.application_id;`
  },
  submit_application: {
    title: "Application preview",
    sql: `INSERT INTO AdoptionApplication (user_id, pet_id, status, submitted_at, notes)\nVALUES (<user_id>, <pet_id>, 'Pending', CURRENT_TIMESTAMP, <notes>);`
  },
  update_application_status: {
    title: "Status update preview",
    sql: `UPDATE AdoptionApplication\nSET status = <new_status>\nWHERE application_id = <application_id>;`
  }
};

function initializePetData(data) {
  console.log(data);
  pets.splice(0, pets.length, ...data);
  syncPetAvailabilityWithApprovals();
  populateApplicationOptions();
  actions.view_all_pets();
}

async function loadPets() {
  showNotice("Loading pet data from pets.json...");

  const candidatePaths = ["pets.json", "./pets.json", "/javascript_frontend/pets.json"];

  for (const path of candidatePaths) {
    try {
      const res = await fetch(path);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      initializePetData(data);
      setMessage(`Loaded pet data from ${path}.`);
      return;
    } catch (error) {
      console.warn(`Unable to load ${path}:`, error);
    }
  }

  if (window.location.protocol === "file:") {
    initializePetData(fallbackPets);
    setMessage("Loaded fallback pet data. For fetch() to read pets.json, open the page through a local server.");
    return;
  }

  console.error("Error loading pets.json from all known paths.");
  showNotice("Unable to load pet data from pets.json. Use http://127.0.0.1:8000/javascript_frontend/index.html.");
  setMessage("Pet data could not be loaded.");
}

const actions = {
  view_all_pets: () => {
    renderQueryResult(
      pets,
      ["pet_id", "name", "species", "age", "available"],
      "view_all_pets",
      "Showing all pets loaded from pets.json."
    );
  },
  view_available_pets: () => {
    const rows = pets.filter((pet) => pet.available);
    renderQueryResult(
      rows,
      ["pet_id", "name", "species", "age", "available"],
      "view_available_pets",
      "Showing only pets that are currently available."
    );
  },
  count_applications_per_pet: () => {
    const rows = pets.map((pet) => ({
      pet_id: pet.pet_id,
      pet_name: pet.name,
      application_count: applications.filter((app) => app.pet_id === pet.pet_id).length
    }));

    renderQueryResult(
      rows,
      ["pet_id", "pet_name", "application_count"],
      "count_applications_per_pet",
      "Showing the number of applications for each pet."
    );
  },
  view_approved_applications: () => {
    const rows = applications.filter((app) => app.status === "Approved");
    renderQueryResult(
      rows,
      ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
      "view_approved_applications",
      "Showing approved adoption applications only."
    );
  },
  view_all_applications: () => {
    renderQueryResult(
      applications,
      ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
      "view_all_applications",
      "Showing all adoption applications."
    );
  },
  query_6_sample: () => {
    const rows = applications.filter((app) => app.pet_id === 101);
    renderQueryResult(
      rows,
      ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
      "view_applications_by_pet",
      "Showing Query 6 for pet_id = 101."
    );
  },
  query_7_sample: () => {
    const rows = applications.filter((app) => app.user_id === 1);
    renderQueryResult(
      rows,
      ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"],
      "view_applications_by_user",
      "Showing Query 7 for user_id = 1."
    );
  },
  view_named_applications: () => {
    const rows = applications.map((application) => ({
      application_id: application.application_id,
      user_name: users.find((user) => user.user_id === application.user_id)?.name ?? "Unknown user",
      pet_name: pets.find((pet) => pet.pet_id === application.pet_id)?.name ?? "Unknown pet",
      status: application.status,
      submitted_at: application.submitted_at,
      notes: application.notes
    }));

    renderQueryResult(
      rows,
      ["application_id", "user_name", "pet_name", "status", "submitted_at", "notes"],
      "view_named_applications",
      "Showing each application with the user and pet names."
    );
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

  const formData = Object.fromEntries(new FormData(event.target).entries());
  const userId = Number(formData.user_id);
  const petId = Number(formData.pet_id);
  const user = users.find((entry) => entry.user_id === userId);
  const pet = pets.find((entry) => entry.pet_id === petId);

  showQuery("submit_application");

  if (!user || !pet) {
    showNotice("Please choose a valid user and an available pet.");
    setMessage("The new application could not be created from the current selections.");
    return;
  }

  const nextId = getNextApplicationId();
  const newApplication = {
    application_id: nextId,
    user_id: userId,
    pet_id: petId,
    status: "Pending",
    submitted_at: getCurrentTimestamp(),
    notes: formData.notes?.trim() || null
  };

  applications.push(newApplication);
  event.target.reset();
  populateApplicationOptions();

  renderTable(
    [newApplication],
    ["application_id", "user_id", "pet_id", "status", "submitted_at", "notes"]
  );
  setMessage(`Application ${nextId} was submitted successfully for ${user.name} to adopt ${pet.name}.`);
});

function renderQueryResult(rows, columns, queryKey, message) {
  syncPetAvailabilityWithApprovals();
  showQuery(queryKey);
  renderTable(rows, columns);
  setMessage(message);
}

function syncPetAvailabilityWithApprovals() {
  pets.forEach((pet) => {
    pet.available = !applications.some(
      (application) => application.pet_id === pet.pet_id && application.status === "Approved"
    );
  });
}

function populateApplicationOptions() {
  syncPetAvailabilityWithApprovals();

  userSelect.innerHTML = users
    .map((user) => `<option value="${user.user_id}">${user.user_id} - ${user.name}</option>`)
    .join("");

  const availablePets = pets.filter((pet) => pet.available);
  petSelect.innerHTML = availablePets
    .map((pet) => `<option value="${pet.pet_id}">${pet.pet_id} - ${pet.name} (${pet.species})</option>`)
    .join("");
}

function getNextApplicationId() {
  return Math.max(...applications.map((application) => application.application_id)) + 1;
}

function getCurrentTimestamp() {
  return new Date().toISOString().slice(0, 19).replace("T", " ");
}

function showQuery(queryKey) {
  const entry = queryCatalog[queryKey];
  queryTitle.textContent = entry?.title ?? "Select a query to preview the SQL.";
  queryPreview.textContent = entry?.sql ?? "";
}

function setMessage(message) {
  statusMessage.textContent = `${message} Data source: pets.json.`;
}

function showNotice(message) {
  results.innerHTML = `<p class="notice">${message}</p>`;
}

function renderTable(rows, columns) {
  if (!rows.length) {
    results.innerHTML = '<p class="notice">No records found for this query.</p>';
    return;
  }

  const headerRow = columns.map((column) => `<th>${column}</th>`).join("");
  const bodyRows = rows
    .map((row) => {
      const cells = columns.map((column) => `<td>${formatValue(row[column])}</td>`).join("");
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

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "NULL";
  }

  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }

  return String(value);
}

loadPets();
