from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from database import metadata


api_flow_json = Table(
    "my_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String)
)
