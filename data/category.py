import sqlalchemy
from data.db_session import SqlAlchemyBase, create_session


association_table = sqlalchemy.Table(
    'category_of_masters',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('Masters', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('Masters.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('category.id'))
)


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


def create_category():
    s = create_session()
    categories = [Category(name='hairdresser'), Category(name='manicure'), Category(name='makeup')]
    for c in categories:
        s.add(c)
    s.commit()
