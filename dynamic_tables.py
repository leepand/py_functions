from peewee import *
d = "/Users/leepand/Downloads/github/vue/vue-admin-flask-example/algolink_ui_server/files/localdb/localdb3-v1/model_samples.db"
db = SqliteDatabase(d)
import datetime

def get_log_model(prefix):
    table_name = 'log_%s' % str(prefix)

    LOG_LEVELS = (
        (0, 'DEBUG'),
        (10, 'INFO'),
        (20, 'WARNING'),
    )

    class LogMetaclass(Model):
        def __new__(cls, name, bases, attrs):
            name += '_' + prefix  # 这是Model的name.
            return Model.__new__(cls, name, bases, attrs)

    class Log(Model):
        __metaclass__ = LogMetaclass
        level = IntegerField(choices=LOG_LEVELS)
        msg = TextField()
        time = DateTimeField(default=datetime.datetime.now)

        @staticmethod
        def is_exists():
            return db.table_exists(table_name)#table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name
            database=db
            
    #db.connect()
    db.create_tables([Log])
    #db.close()
    return Log

cls=get_log_model("ahah")

log = cls(level=10, msg="Hello")
log.save()
