# Spec: Registration

## Overview
This step wires up the `POST /register` route so users can actually create accounts.
The `GET /register` route and `register.html` template already exist with a working form,
but form submission currently hits a missing handler. This step adds the server-side
processing: validate inputs, check for duplicate email, hash the password, insert the
user row, and redirect to `/login` on success. It also adds the two DB helper functions
(`create_user`, `get_user_by_email`) that authentication steps will reuse.

## Depends on
- Step 01 — Database Setup (`get_db()`, `init_db()`, schema for `users` table)

## Routes
- `GET /register` — already implemented, no change
- `POST /register` — process registration form — public

## Database changes
No new tables or columns. Two new helper functions in `database/db.py`:
- `get_user_by_email(email)` — returns a `Row` or `None`
- `create_user(name, email, password)` — hashes password and inserts row; returns nothing

## Templates
- **Modify:** `templates/register.html`
  - Fix hardcoded `action="/register"` → `action="{{ url_for('register') }}"`
  - Re-populate `name` and `email` fields with `value="{{ request.form.name }}"` etc. on error so the user doesn't retype everything

## Files to change
- `app.py` — add `POST` method to `/register` route; import `request`, `redirect`, `url_for`, `flash` from flask; set `app.secret_key`
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — fix action URL; re-populate fields on error

## Files to create
None.

## New dependencies
No new pip packages. `werkzeug.security.generate_password_hash` is already imported in `database/db.py`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterized queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` inside `create_user()`; the route must never hash inline
- `app.secret_key` must be set before any `flash()` or session use; use a hard-coded dev string for now (e.g. `"dev-secret-change-me"`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Pass `error` directly to `render_template()` on failure — do not use `flash()` for form errors (template already has `{% if error %}`)
- On success: redirect to `url_for('login')` — do not log the user in yet (that's Step 3)
- Use `abort(400)` only for genuinely malformed requests; for user-correctable errors (duplicate email, short password) re-render the form with `error`

## Validation rules
1. `name` — required, non-empty after `.strip()`
2. `email` — required; if already in `users` table → error "An account with that email already exists."
3. `password` — required, minimum 8 characters; shorter → error "Password must be at least 8 characters."

## Definition of done
- [ ] Submitting the form with valid data creates a new row in `users` with a hashed password and redirects to `/login`
- [ ] Submitting with an email that already exists re-renders the form with an error message and does not insert a duplicate row
- [ ] Submitting with a password shorter than 8 characters re-renders the form with an error message
- [ ] `name` and `email` fields are re-populated on validation error so the user doesn't retype
- [ ] The `action` attribute in `register.html` uses `url_for('register')`, not a hardcoded URL
- [ ] `get_user_by_email()` and `create_user()` live in `database/db.py`, not in `app.py`
- [ ] App starts without errors and `GET /register` still renders the empty form
