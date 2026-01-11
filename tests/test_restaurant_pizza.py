import pytest
from app import create_app, db
from app.models import Restaurant, Pizza, RestaurantPizza


@pytest.fixture
def client(tmp_path):
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # seed minimal data
        r = Restaurant(name='Test R', capacity=10)
        p = Pizza(name='Test P', ingredients='ing')
        db.session.add_all([r, p])
        db.session.commit()
    with app.test_client() as c:
        yield c


def test_get_restaurants(client):
    rv = client.get('/restaurants')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_get_pizzas(client):
    rv = client.get('/pizzas')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)


def test_create_restaurant_pizza(client):
    # create using seeded ids 1 and 1
    rv = client.post('/restaurant_pizzas', json={'price': 9, 'restaurant_id': 1, 'pizza_id': 1})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['price'] == 9
    assert 'pizza' in data and 'restaurant' in data


def test_delete_restaurant(client):
    rv = client.delete('/restaurants/1')
    assert rv.status_code == 200
    # subsequent get should 404
    rv2 = client.get('/restaurants/1')
    assert rv2.status_code == 404
