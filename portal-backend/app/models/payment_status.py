from ..db import db

class PaymentStatus(db.Model):
    __tablename__ = 'payment_statuses'

    paymentstatusid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    leases = db.relationship('Lease', backref='payment_status', lazy=True)

    def __repr__(self):
        return f"<PaymentStatus {self.description}>"