# lateshow-david-kamau

Local Flask API for episodes, guests, and appearances.

Setup
1. Create and activate a Python virtualenv.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize migrations and migrate (optional):

```bash
flask db init  # run once if using migrations
flask db migrate -m "initial"
flask db upgrade
```

Or run the helper to call Alembic upgrade (requires Flask-Migrate config):

```bash
python manage.py migrate
```

4. Seed the database:

```bash
python seed.py
```

Run

```bash
python manage.py
```

API Endpoints
- `GET /episodes` - list episodes (id, date, number)
- `GET /episodes/<id>` - episode with appearances and guest details
- `GET /guests` - list guests
- `POST /appearances` - create appearance with JSON {"rating":int, "episode_id":int, "guest_id":int}
