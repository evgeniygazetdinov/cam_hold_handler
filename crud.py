from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, customer_name: str):
    return db.query(models.User).filter(models.User.customer_name == customer_name).first()
