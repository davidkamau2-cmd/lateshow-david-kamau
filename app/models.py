from . import db


class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship(
        'Appearance', back_populates='episode', cascade='all, delete-orphan'
    )

    def to_dict(self, include=None, exclude=None, depth=1):
        data = {'id': self.id, 'date': self.date, 'number': self.number}
        if depth and (include is None or 'appearances' in include):
            data['appearances'] = [a.to_dict(include=('guest',), depth=depth-1) for a in self.appearances]
        return data


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    appearances = db.relationship(
        'Appearance', back_populates='guest', cascade='all, delete-orphan'
    )

    def to_dict(self, include=None, exclude=None, depth=1):
        return {'id': self.id, 'name': self.name, 'occupation': self.occupation}


class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    def to_dict(self, include=None, exclude=None, depth=1):
        data = {
            'id': self.id,
            'rating': self.rating,
            'guest_id': self.guest_id,
            'episode_id': self.episode_id,
        }
        if depth and include and 'guest' in include:
            data['guest'] = self.guest.to_dict()
        if depth and include and 'episode' in include:
            # return episode base fields only
            data['episode'] = {'id': self.episode.id, 'date': self.episode.date, 'number': self.episode.number}
        return data
