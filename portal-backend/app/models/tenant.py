from ..db import db

class Tenant(db.Model):
    __tablename__ = 'tenants'

    tenantid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contactinfo = db.Column(db.String(100), nullable=False)

    leases = db.relationship('Lease', backref='tenant', lazy=True)

    def __repr__(self):
        return f"<Tenant {self.name}>"