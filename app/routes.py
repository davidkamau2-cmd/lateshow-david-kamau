from flask import Blueprint, jsonify, request
from .models import Episode, Guest, Appearance
from . import db

bp = Blueprint('api', __name__)


@bp.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict(depth=0) for e in episodes])


@bp.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    ep = Episode.query.get(episode_id)
    if not ep:
        return jsonify({'error': 'Episode not found'}), 404
    return jsonify(ep.to_dict())


@bp.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests])


@bp.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json() or {}
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    errors = []
    if rating is None:
        errors.append('rating is required')
    else:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                errors.append('rating must be between 1 and 5')
        except Exception:
            errors.append('rating must be an integer')

    if episode_id is None:
        errors.append('episode_id is required')
    if guest_id is None:
        errors.append('guest_id is required')

    if errors:
        return jsonify({'errors': errors}), 422

    episode = Episode.query.get(episode_id)
    guest = Guest.query.get(guest_id)
    if not episode:
        return jsonify({'errors': ['episode not found']}), 422
    if not guest:
        return jsonify({'errors': ['guest not found']}), 422

    appearance = Appearance(rating=rating, episode=episode, guest=guest)
    db.session.add(appearance)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 422

    return jsonify(appearance.to_dict(include=('episode', 'guest'), depth=1)), 201
