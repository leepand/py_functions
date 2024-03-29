# https://www.dongwm.com/post/118/
from datetime import datetime

from sqlalchemy import Column, DateTime
from flask_sqlalchemy import SQLAlchemy, Model


class BaseModel(Model):
    # create_at这个属性也是创建表结构默认都包含的
    create_at = Column(DateTime, default=datetime.utcnow())

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}


db = SQLAlchemy(model_class=BaseModel)
