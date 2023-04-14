import string
from http import HTTPStatus
from random import choice

from flask import abort, flash, redirect, render_template
from settings import SHORT_URL_LENGTH

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id(length: int):
    letters = string.ascii_letters + string.digits
    custom_id_generated = ''.join([choice(letters) for _ in range(length)])
    while URLMap.query.filter_by(short=custom_id_generated).first():
        custom_id_generated = ''.join([choice(letters) for _ in range(length)])
    return custom_id_generated


def get_url_map(original_link: str, custom_id: str) -> URLMap:
    custom_id = custom_id or get_unique_short_id(SHORT_URL_LENGTH)
    url_map = URLMap(original=original_link, short=custom_id)
    if URLMap.query.filter_by(original=original_link).first():
        url_map.errors['original_link'] = ['Имя py уже занято!']
    if URLMap.query.filter_by(short=custom_id).first():
        url_map.errors['custom_id'] = ['Такая коротка ссылка уже существует!']
    return url_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = get_url_map(form.original_link.data, form.custom_id.data)
        if custom_id.errors['original_link'] or custom_id.errors['custom_id']:
            form.original_link.errors.extend(custom_id.errors['original_link'])
            form.custom_id.errors.extend(custom_id.errors['custom_id'])
            return render_template('index.html', form=form)
        db.session.add(custom_id)
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'information-message')
        flash(custom_id.short, 'url')
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    custom_id = URLMap.query.filter_by(short=custom_id).first()
    if custom_id:
        return redirect(custom_id.original)
    abort(HTTPStatus.NOT_FOUND)
