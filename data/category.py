import sqlalchemy
from data.db_session import SqlAlchemyBase, create_session

# Вспомогательная таблица для Категорий Мастеров
association_table = sqlalchemy.Table(
    'Category_of_Masters',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('Masters', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('Masters.id')),
    sqlalchemy.Column('Category', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('Category.id'))
)


# Таблица Категорий
class Category(SqlAlchemyBase):
    __tablename__ = 'Category'  # Имя таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)  # id
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя Категории

    def __repr__(self):
        return f'{self.name}'


# костыль
def create_category():
    s = create_session()
    categories = [Category(name='Мастер маникюра(педикюра)'), Category(name='Парикмахер'), Category(name='Визажист')]
    for c in categories:
        s.add(c)
    s.commit()
