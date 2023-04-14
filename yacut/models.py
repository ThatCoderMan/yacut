from collections import defaultdict
from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False, unique=True)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = defaultdict(list)

    def to_dict(self):
        return dict(url=self.original, short_link=url_for(
            'redirect_view',
            custom_id=self.short,
            _external=True
        ))
