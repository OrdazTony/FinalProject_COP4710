# Front End Viewing Instructions

This project currently includes two separate front-end prototypes for the Pet Adoption Management System:

- `javascript_frontend/` — simple browser-based UI prototype
- `pyqt_frontend/` — simple PyQt desktop UI prototype

Both are **view-only prototypes** right now and are **not yet connected** to the Python backend/database logic.

---

## 1. View the JavaScript Front End

### Files
- `javascript_frontend/index.html`
- `javascript_frontend/styles.css`
- `javascript_frontend/app.js`
- `javascript_frontend/pets.json`

### Recommended: run with a local server
Because the page uses `fetch("pets.json")`, opening `index.html` directly with `file://` may cause the browser to block the request.

From the project root:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/javascript_frontend/index.html
```

### Optional: direct open for a quick fallback preview
You can still double-click `index.html`, but some browsers will block `fetch()` and the page will fall back to built-in sample pet data instead of loading `pets.json` directly.

---

## 2. Run the PyQt Front End

### Files
- `pyqt_frontend/pyqt_frontend.py`
- `pyqt_frontend/requirements.txt`

### Steps
From the project root:

```bash
cd pyqt_frontend
pip install -r requirements.txt
python pyqt_frontend.py
```

If your system uses `python3`, run:

```bash
cd pyqt_frontend
pip install -r requirements.txt
python3 pyqt_frontend.py
```

---

## Notes

- The JavaScript front end is best for a quick visual browser mockup.
- The PyQt front end is a desktop-style prototype.
- Neither one is fully functional yet; they are intended for layout/demo purposes only.
