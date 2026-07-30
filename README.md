# Supervisor Finder

A coursework prototype that helps final-year students discover supervisors and project ideas, while allowing staff to maintain their own public profiles.

## Technology

- **Python**: application and validation rules.
- **Flask**: web framework that maps browser URLs to Python functions.
- **SQLite**: file-based relational database, included with Python.
- **HTML/CSS**: page structure and visual design.
- **unittest**: automated tests supplied with Python.

The project follows a lightweight layered/MVC design: templates form the presentation layer, `app.py` contains route/controller and business rules, and SQLite is the persistence layer.

## Run in VS Code

1. Open this folder in VS Code.
2. In the integrated terminal, create an isolated Python environment: `python3 -m venv .venv`.
3. Activate it with `source .venv/bin/activate` (macOS/Linux) or `.venv\\Scripts\\activate` (Windows).
4. Install the one dependency: `python3 -m pip install -r requirements.txt`.
5. Run `python3 app.py`, then visit `http://127.0.0.1:5000`.

The first run creates `instance/supervisor_finder.db` and inserts demonstration data.

## Demo staff account

- Email: `ada@university.ac.uk`
- Password: `demo123`

This is only a development demonstration account. A production system would use a university single-sign-on provider and securely managed passwords.

## Tests

Run `python3 -m unittest discover -s tests -v`.

## Core features

- Browse, search and filter staff by interest area.
- View detailed staff and project profiles.
- Save project ideas for later during a browsing session.
- Authenticate as staff and manage a personal profile, areas of interest and project ideas.
- Validate user input and prevent staff from changing another member's content.
