# Импортирование модулей для работы с ORM
from peewee import (Model, SqliteDatabase)

# создаем экземпляр класса для работы с системой SQLite
db = SqliteDatabase('DocumentsStorage.db')


# Базовый класс базы данных
class BaseModel(Model):
    class Meta:
        database = db