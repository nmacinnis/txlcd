import contextlib
import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()


class Model(object):
    def __init__(self, logger=None, datastore=None):
        self.logger = logger
        self.sessionmaker = self._init_db(datastore)

    @contextlib.contextmanager
    def _autoclosing_session(self):
        session = self.sessionmaker()
        try:
            try:
                yield session
            except:
                session.rollback()
                raise
        finally:
            session.close()

    def _init_db(self, datastore):
        engine = sqlalchemy.engine.create_engine(datastore)
        Base.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(
            bind=engine,
            autoflush=True
        )

    def get_latest_message(self):
        with self._autoclosing_session() as session:
            return session.query(Message).\
                    order_by(Message.message_id.desc()).\
                    first()

    def get_previous_message(self, message_id):
        with self._autoclosing_session() as session:
            return session.query(Message).\
                    filter(Message.message_id < message_id).\
                    order_by(Message.message_id.desc()).\
                    first()

    def get_next_message(self, message_id):
        with self._autoclosing_session() as session:
            return session.query(Message).\
                    filter(Message.message_id > message_id).\
                    order_by(Message.message_id.asc()).\
                    first()

    def add_message(self, message_text):
        with self._autoclosing_session() as session:
            message = Message(message_text=message_text)
            session.add(message)
            session.commit()

    def delete_message(self, message_id):
        with self._autoclosing_session() as session:
            message = session.query(Message).\
                    get(message_id)
            session.delete(message)
            session.commit()



class Message(Base):
    __tablename__ = 'messages'

    message_id = sqlalchemy.Column(
        sqlalchemy.types.Integer(),
        primary_key=True,
        index=True,
    )

    message_text = sqlalchemy.Column(
        sqlalchemy.types.String(1024),
        nullable=False
    )
