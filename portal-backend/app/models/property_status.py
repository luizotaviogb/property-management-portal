from ..db import db

class PropertyStatus(db.Model):
    __tablename__ = 'property_statuses'

    propertystatusid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    properties = db.relationship('Property', backref='property_status', lazy=True)

    def __repr__(self):
        return f"<PropertyStatus {self.description}>"