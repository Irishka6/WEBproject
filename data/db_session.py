import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.pool import QueuePool

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'sqlite:///db/db.sqlite?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, poolclass=QueuePool)
    __factory = orm.sessionmaker(bind=engine)

    from data import __all_models__

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


global_init()
db_sess = create_session()
