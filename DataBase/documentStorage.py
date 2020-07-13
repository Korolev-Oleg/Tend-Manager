# Импортирование модулей для работы с ORM
from peewee import (Model, CharField, SqliteDatabase,
                    BooleanField, TextField, ForeignKeyField)

# создаем экземпляр класса для работы с системой SQLite
db = SqliteDatabase('DocumentsStorage.db')


# Базовый класс базы данных
class BaseModel(Model):
    class Meta:
        database = db


# сущность методов закупок
class Methods(BaseModel):
    name = CharField(max_length=250)


# сущность категорий товаров
class Categories(BaseModel):
    name = CharField(max_length=250)


# сущность списка документов
class DocumentList(BaseModel):
    name = CharField(max_length=250)
    checked = BooleanField()
    method = ForeignKeyField(model=Methods)
    category = ForeignKeyField(model=Categories)
    source = TextField()
    law = CharField(choices=(['223 ФЗ', 223], ['44 ФЗ', 44]))


# Сущность списка выполненных заявок
class CompletedApps(BaseModel):
    name = CharField()
    category = ForeignKeyField(model=Categories)
    dest_path = TextField()


db.connect()
db.create_tables([Methods, Categories, DocumentList, CompletedApps])
db.commit()
