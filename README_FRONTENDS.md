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

### Option A: Open directly in a browser
1. Open the `javascript_frontend` folder.
2. Double-click `index.html`.
3. Or right-click and open it in your browser.

### Option B: Open from terminal
From the project root:

```bash
open javascript_frontend/index.html
```

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
