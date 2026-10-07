from functools import wraps
from app.model import db


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
