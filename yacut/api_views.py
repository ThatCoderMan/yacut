import re
from http import HTTPStatus

from flask import jsonify, request
from settings import SHORT_URL_LENGTH

from . import app, db
from .error_handler import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    original = URLMap.query.filter_by(short=short_id).first()
    if original is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original.original}), HTTPStatus.OK


def get_api_url_map(original_link: str, custom_id: str) -> URLMap:
    custom_id = custom_id or get_unique_short_id(SHORT_URL_LENGTH)

    if len(custom_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if re.match(r"^[A-Za-z0-9]+$", custom_id) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    if not original_link:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=original_link).first() is not None:
        raise InvalidAPIUsage(f'Имя "{original_link}" уже занято.')

    return URLMap(original=original_link, short=custom_id)


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    custom_id = get_api_url_map(data.get('url'), data.get('custom_id'))
    db.session.add(custom_id)
    db.session.commit()
    return jsonify(custom_id.to_dict()), HTTPStatus.CREATED
