from functools import wraps
from app.main import db


def transactional(operation):
    @wraps(operation)
    def wrapped(*args, **kwargs):
        try:
            result = operation(*args, **kwargs)
            db.session.commit()
            return result
        except Exception:
            db.session.rollback()
            raise
    return wrapped


def rollback_session():
    db.session.rollback()
