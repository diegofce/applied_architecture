from sqlalchemy.orm import sessionmaker

from todo_app.infrastructure.database.models import Base


def initialize_database(session_factory: sessionmaker) -> None:
    engine = session_factory.kw["bind"]
    Base.metadata.create_all(bind=engine)
