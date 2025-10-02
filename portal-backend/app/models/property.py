from ..db import db
from datetime import date

class Property(db.Model):
    __tablename__ = 'properties'

    propertyid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    propertytypeid = db.Column(db.Integer, db.ForeignKey('property_types.propertytypeid'), nullable=False)
    propertystatusid = db.Column(db.Integer, db.ForeignKey('property_statuses.propertystatusid'), nullable=False)
    purchasedate = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(15, 2), nullable=False)

    leases = db.relationship('Lease', backref='property', lazy=True)
    maintenance_tasks = db.relationship('Maintenance', backref='property', lazy=True)

    def __repr__(self):
        return f"<Property {self.address}>"