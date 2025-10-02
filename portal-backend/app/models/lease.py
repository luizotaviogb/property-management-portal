from ..db import db
from datetime import date

class Lease(db.Model):
    __tablename__ = 'leases'

    leaseid = db.Column(db.Integer, primary_key=True)
    tenantid = db.Column(db.Integer, db.ForeignKey('tenants.tenantid'), nullable=False)
    propertyid = db.Column(db.Integer, db.ForeignKey('properties.propertyid'), nullable=False)
    leasetermstart = db.Column(db.Date, nullable=False)
    leasetermend = db.Column(db.Date, nullable=False)
    paymentstatusid = db.Column(db.Integer, db.ForeignKey('payment_statuses.paymentstatusid'), nullable=False)

    def __repr__(self):
        return f"<Lease {self.leaseid}>"
