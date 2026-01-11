from app import create_app, db
from flask_migrate import upgrade


app = create_app()


def run_migrations():
    """Run migrations (calls Alembic upgrade head)."""
    with app.app_context():
        upgrade()


if __name__ == '__main__':
    # handy entrypoint: python manage.py migrate
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ('migrate', 'upgrade'):
        run_migrations()
    else:
        app.run(debug=True)
