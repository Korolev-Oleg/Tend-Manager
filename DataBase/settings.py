# Импортирование модулей для работы с ORM
from peewee import (Model, CharField, SqliteDatabase,
                    BooleanField, TextField, ForeignKeyField)

# создаем экземпляр класса для работы с системой SQLite
db = SqliteDatabase('settings.db')


# Базовый класс базы данных
class BaseModel(Model):
    class Meta:
        database = db


# Модель шаблонов расчетных документов
class Payments(BaseModel):
    name = CharField(max_length=250)
    path = TextField()


# Модель основных настроек
class General(BaseModel):
    main_path = TextField()
    shared_path = TextField()
    payment_source = ForeignKeyField(model=Payments)
    sheet_name = CharField(max_length=250)
    cell_top_left = CharField(max_length=8)
    cell_bot_down = CharField(max_length=8)
    open_folder = BooleanField()
    open_payment = BooleanField()
    wnd_on_top = BooleanField()
    wnd_animation = BooleanField()
    wnd_position = TextField(choices=(
        ['Свободное перемещение', 0], ['Закреплено слева', 1],
        ['Закреплено справа', 2]))


# Модель конечных путей
class PathDestinationModel(BaseModel):
    static_dist = TextField()
    dynamic_dist = TextField()
    payment_dist = TextField()
    other_dist = TextField()

