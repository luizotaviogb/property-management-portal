from ..db import db
from datetime import date

class Tenant(db.Model):
    __tablename__ = 'tenants'

    tenantid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contactinfo = db.Column(db.String(100), nullable=False)
    leasetermstart = db.Column(db.Date, nullable=False)
    leasetermend = db.Column(db.Date, nullable=False)
    paymentstatusid = db.Column(db.Integer, db.ForeignKey('payment_statuses.paymentstatusid'), nullable=False)
    propertyid = db.Column(db.Integer, db.ForeignKey('properties.propertyid'), nullable=False)

    def __repr__(self):
        return f"<Tenant {self.name}>"