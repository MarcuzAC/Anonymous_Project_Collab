from datetime import datetime
from models import db

class Tip(db.Model):
    __tablename__ = 'tip'
    id = db.Column(db.Integer, primary_key=True)
    corruption_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    date = db.Column(db.String(20))
    people = db.Column(db.String(200))
    tip_category = db.Column(db.String(100))
    description = db.Column(db.Text)
    file = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
