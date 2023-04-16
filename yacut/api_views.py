import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handler import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    original = URLMap.query.filter_by(short=short_id).first()
    if original is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': original.original}), HTTPStatus.OK


def get_api_url_map(original_link: str, custom_id: str) -> URLMap:
    url_map = URLMap(original=original_link, short=custom_id)
    if len(url_map.short) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if re.match(r"^[A-Za-z0-9]+$", url_map.short) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=url_map.short).first() is not None:
        raise InvalidAPIUsage(f'Имя "{url_map.short}" уже занято.')

    if not url_map.original:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if URLMap.query.filter_by(original=url_map.original).first() is not None:
        raise InvalidAPIUsage(f'Имя "{url_map.original}" уже занято.')

    return url_map


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    custom_id = get_api_url_map(data.get('url'), data.get('custom_id'))
    db.session.add(custom_id)
    db.session.commit()
    return jsonify(custom_id.to_dict()), HTTPStatus.CREATED
