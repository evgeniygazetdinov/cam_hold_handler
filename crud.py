from sqlalchemy.orm import Session

import models, schemas


def get_user_by_email(db: Session, customer_name: str):
    return db.query(models.api_flow_json).filter(models.api_flow_json.columns.customer_name == str(customer_name)).first()
