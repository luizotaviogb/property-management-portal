from ..db import db

class MaintenanceStatus(db.Model):
    __tablename__ = 'maintenance_statuses'

    maintenancestatusid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), unique=True, nullable=False)

    maintenance_tasks = db.relationship('Maintenance', backref='maintenance_status', lazy=True)

    def __repr__(self):
        return f"<MaintenanceStatus {self.description}>"