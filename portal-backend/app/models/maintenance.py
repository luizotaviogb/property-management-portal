from ..db import db
from datetime import date

class Maintenance(db.Model):
    __tablename__ = 'maintenance'

    taskid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    maintenancestatusid = db.Column(db.Integer, db.ForeignKey('maintenance_statuses.maintenancestatusid'), nullable=False)
    scheduleddate = db.Column(db.Date, nullable=False)
    propertyid = db.Column(db.Integer, db.ForeignKey('properties.propertyid'), nullable=False)

    def __repr__(self):
        return f"<Maintenance {self.description}>"