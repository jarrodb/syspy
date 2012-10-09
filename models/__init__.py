from sqlalchemy import create_engine
from settings import settings

from base import Base
import postfix
import auth

engine = create_engine(
    '%s://%s:%s@%s/%s' % (
        settings.sql_ngin,
        settings.sql_user,
        settings.sql_pass,
        settings.sql_host,
        settings.sql_dbnm,
    ))

metadata = Base.metadata
metadata.create_all(engine)

