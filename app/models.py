from datetime import datetime

from app import db


class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    product = db.Column(db.String(140))
    cost = db.Column(db.Float)
    price = db.Column(db.Float, default=cost/amount)
    place = db.Column(db.String(140))
    product_type = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return f'{self.product} cost {round(self.price, 2)} in {self.place}'
