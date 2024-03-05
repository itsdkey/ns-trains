from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

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
