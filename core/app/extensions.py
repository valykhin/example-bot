from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from prometheus_flask_exporter import PrometheusMetrics
from flask_apscheduler import APScheduler
from flask_httpauth import HTTPBasicAuth


class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin, session_options={'expire_on_commit': False})
migrate = Migrate()
metrics = PrometheusMetrics.for_app_factory()
scheduler = APScheduler()
auth = HTTPBasicAuth()


