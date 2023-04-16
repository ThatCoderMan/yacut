import string
from collections import defaultdict
from datetime import datetime
from random import choice

from flask import url_for
from settings import SHORT_URL_LENGTH

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = defaultdict(list)
        if not self.short:
            self.generate_unique_short_id(SHORT_URL_LENGTH)

    def to_dict(self):
        return dict(url=self.original, short_link=url_for(
            'redirect_view',
            custom_id=self.short,
            _external=True
        ))

    def generate_unique_short_id(self, length: int):
        letters = string.ascii_letters + string.digits
        self.short = ''.join([choice(letters) for _ in range(length)])
        while self.query.filter_by(short=self.short).first():
            self.short = ''.join(
                [choice(letters) for _ in range(length)]
            )
