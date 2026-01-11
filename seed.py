from app import create_app, db
from app.models import Episode, Guest, Appearance


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Clear existing
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()

        # Episodes
        e1 = Episode(date='1/11/99', number=1)
        e2 = Episode(date='1/12/99', number=2)
        db.session.add_all([e1, e2])

        # Guests
        g1 = Guest(name='Michael J. Fox', occupation='actor')
        g2 = Guest(name='Sandra Bernhard', occupation='Comedian')
        g3 = Guest(name='Tracey Ullman', occupation='television actress')
        db.session.add_all([g1, g2, g3])
        db.session.commit()

        # Appearances
        a1 = Appearance(rating=4, episode=e1, guest=g1)
        a2 = Appearance(rating=5, episode=e2, guest=g3)
        db.session.add_all([a1, a2])
        db.session.commit()

        print('Seeded database with sample data')


if __name__ == '__main__':
    seed()
