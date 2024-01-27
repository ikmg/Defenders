from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


class Connection:

    def __init__(self, db_uri, echo=False):
        self.db_uri = db_uri
        self.engine = create_engine(db_uri, echo=echo)
        _session_ = sessionmaker(bind=self.engine)
        self.session = _session_()

    def __repr__(self):
        return self.db_uri

    def create_db(self):
        Base.metadata.create_all(self.engine)
    #
    # def drop_db(self):
    #     print('<{}> полная очистка...'.format(self.db_uri))
    #     Base.metadata.drop_all(self.engine)
    #
    # def recreate_db(self):
    #     self.drop_db()
    #     print('<{}> создание...'.format(self.db_uri))
    #     self.create_db()
