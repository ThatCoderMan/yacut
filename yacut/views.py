import string
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


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(original=original_link).first():
            form.original_link.errors.append('Имя py уже занято!')
            return render_template('index.html', form=form)
        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                form.custom_id.errors.append(
                    'Такая коротка ссылка уже существует!'
                )
                return render_template('index.html', form=form)
        else:
            custom_id = get_unique_short_id(SHORT_URL_LENGTH)
        db.session.add(URLMap(original=original_link, short=custom_id))
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'information-message')
        flash(custom_id, 'url')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    custom_id = URLMap.query.filter_by(short=custom_id).first()
    if custom_id:
        return redirect(custom_id.original)
    abort(404)
