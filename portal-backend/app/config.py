import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@db:5432/property_management'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False