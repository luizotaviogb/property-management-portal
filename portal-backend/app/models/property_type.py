from ..db import db

class PropertyType(db.Model):
    __tablename__ = 'property_types'

    propertytypeid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    properties = db.relationship('Property', backref='property_type', lazy=True)

    def __repr__(self):
        return f"<PropertyType {self.description}>"