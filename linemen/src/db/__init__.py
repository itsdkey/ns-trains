from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Integer, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

db = SQLAlchemy()
migrate = Migrate()

meta = MetaData(
    naming_convention=dict(
        fk="fk__%(table_name)s__%(referred_table_name)s__%(column_0_name)s",
        ck="ck__%(table_name)s__%(column_0_name)s",
        uq="uq__%(table_name)s__%(column_0_name)s",
    )
)
_Base = declarative_base(metadata=meta)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(Integer, primary_key=True)

    created_at = db.Column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    updated_at = db.Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        onupdate=func.now(),
    )
