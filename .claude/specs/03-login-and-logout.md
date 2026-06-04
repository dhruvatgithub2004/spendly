# Spec: Login and Logout

## Overview
This step wires up the `POST /login` route and fully implements `GET /logout` so users
can authenticate and end their session. The `GET /login` route and `login.html` template
already exist with a working form, but form submission currently hits an unhandled GET
handler and the logout stub returns a plain string. This step adds password verification
via `werkzeug`, sets a `session['user_id']` cookie on success, clears it on logout, and
makes the navbar session-aware so logged-in and logged-out states render different links.

## Depends on
- Step 01 — Database Setup (`get_db()`, `init_db()`, `users` table schema)
- Step 02 — Registration (`get_user_by_email()`, `create_user()`)

## Routes
- `GET /login` — already implemented (renders template); add `POST` method only
- `POST /login` — process login form, set session, redirect on success — public
- `GET /logout` — clear session, redirect to landing — public

## Database changes
No new tables or columns. One new helper function in `database/db.py`:
- `get_user_by_id(id)` — returns a `Row` or `None`; needed here to verify sessions and
  reused by the profile step

## Templates
- **Modify:** `templates/login.html`
  - Fix hardcoded `action="/login"` → `action="{{ url_for('login') }}"`
  - Re-populate `email` field with `value="{{ email or '' }}"` on validation error so the
    user does not retype
- **Modify:** `templates/base.html`
  - Make the `<div class="nav-links">` block session-aware:
    - Logged out: show current "Sign in" and "Get started" links
    - Logged in: show the user's name (plain text or a span) and a "Sign out" link pointing
      to `url_for('logout')`

## Files to change
- `app.py` — add `POST` to the `/login` route; import `session` and `check_password_hash`
  from their respective modules; implement `POST /login` handler; replace the `/logout`
  stub with a real implementation
- `database/db.py` — add `get_user_by_id(id)`
- `templates/login.html` — fix action URL; re-populate email on error
- `templates/base.html` — session-aware nav links

## Files to create
None.

## New dependencies
No new pip packages. `werkzeug.security.check_password_hash` is already available via the
existing `werkzeug` install.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterized queries only — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash`; do not implement custom
  hashing logic
- `session` must be imported from `flask`; `app.secret_key` is already set in `app.py` —
  do not change or duplicate it
- Use CSS variables — never hardcode hex values in templates or stylesheets
- All templates extend `base.html`
- Pass `error` directly to `render_template()` on failure — do not use `flash()` for form
  errors (the template already has `{% if error %}`)
- On successful login: `session['user_id'] = user['id']`, then redirect to
  `url_for('profile')` (stub is fine for now; Step 4 will replace it)
- On logout: `session.clear()`, then redirect to `url_for('landing')`
- Use `abort(400)` only for genuinely malformed requests (missing form keys); for
  wrong-password or unknown-email errors, re-render the form with a generic error message
  ("Invalid email or password.") — do not leak which field was wrong

## Validation rules
1. `email` — required; normalise to lowercase with `.strip().lower()`
2. `password` — required; if email not found OR `check_password_hash` fails → same generic
   error ("Invalid email or password.") to prevent user enumeration

## Definition of done
- [ ] Submitting the login form with valid credentials creates a session and redirects to `/profile`
- [ ] Submitting with an unknown email re-renders `login.html` with "Invalid email or password." and does not reveal whether the email exists
- [ ] Submitting with a correct email but wrong password re-renders `login.html` with the same generic error
- [ ] `email` field is re-populated on validation error so the user does not retype
- [ ] `GET /logout` clears the session and redirects to the landing page; visiting it without a session also redirects safely
- [ ] `action` attribute in `login.html` uses `url_for('login')`, not a hardcoded URL
- [ ] Navbar shows "Sign out" (linking to `/logout`) when a session is active; shows "Sign in" and "Get started" when not
- [ ] `get_user_by_id()` lives in `database/db.py`, not in `app.py`
- [ ] App starts without errors and `GET /login` still renders the empty form
