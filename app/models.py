from . import db
from sqlalchemy.orm import validates



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
            # include guest details for each appearance (limit recursion)
            data['appearances'] = [a.to_dict(include=('guest',), depth=1) for a in self.appearances]
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


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    restaurant_pizzas = db.relationship(
        'RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan'
    )

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('name must be present')
        if len(value) > 80:
            raise ValueError('name too long')
        return value

    @validates('capacity')
    def validate_capacity(self, key, value):
        if value is None:
            raise ValueError('capacity must be present')
        if not isinstance(value, int) or value < 0:
            raise ValueError('capacity must be a non-negative integer')
        return value

    def to_dict(self, include=None, exclude=None, depth=1):
        data = {'id': self.id, 'name': self.name, 'capacity': self.capacity}
        if depth and (include is None or 'pizzas' in include):
            data['pizzas'] = [rp.to_dict(include=('pizza',), depth=1) for rp in self.restaurant_pizzas]
        return data


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('name must be present')
        if len(value) > 80:
            raise ValueError('name too long')
        return value

    @validates('ingredients')
    def validate_ingredients(self, key, value):
        if not value or not value.strip():
            raise ValueError('ingredients must be present')
        return value

    def to_dict(self, include=None, exclude=None, depth=1):
        return {'id': self.id, 'name': self.name, 'ingredients': self.ingredients}


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    __table_args__ = (
        db.CheckConstraint('price > 0 AND price <= 1000', name='price_range'),
    )

    @validates('price')
    def validate_price(self, key, value):
        if value is None:
            raise ValueError('price must be present')
        try:
            iv = int(value)
        except Exception:
            raise ValueError('price must be integer')
        if iv <= 0 or iv > 1000:
            raise ValueError('price out of allowed range')
        return iv

    def to_dict(self, include=None, exclude=None, depth=1):
        data = {'id': self.id, 'price': self.price, 'restaurant_id': self.restaurant_id, 'pizza_id': self.pizza_id}
        if depth and include and 'pizza' in include:
            data['pizza'] = self.pizza.to_dict()
        if depth and include and 'restaurant' in include:
            data['restaurant'] = {'id': self.restaurant.id, 'name': self.restaurant.name, 'capacity': self.restaurant.capacity}
        return data
