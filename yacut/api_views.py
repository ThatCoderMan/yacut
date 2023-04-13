import re

from flask import jsonify, request

from . import app, db
from .error_handler import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    original = URLMap.query.filter_by(short=short_id).first()
    if original is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    original_link = data.get('url', None)
    custom_id = data.get('custom_id', '')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if re.match(r"^[A-Za-z0-9]+$", custom_id) is None:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    else:
        custom_id = get_unique_short_id(6)
    if original_link is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=original_link).first() is not None:
        raise InvalidAPIUsage(f'Имя "{original_link}" уже занято.')
    url = URLMap(original=original_link, short=custom_id)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
