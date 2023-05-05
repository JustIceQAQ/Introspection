import pydantic
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel, Field, BaseConfig, Extra
from typing import Optional

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column("Id", Integer, primary_key=True, index=True)
    email = Column("Email", String, unique=True, index=True)
    hashed_password = Column("HashedPassword", String)
    is_active = Column("IsActive", Boolean, default=True)


class CommonBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True


def main():
    user_attr = {
        value.property.columns[0].name: key
        for key, value in User.__dict__.items()
        if hasattr(value, "property")
        if hasattr(value.property, "columns")
    }
    parameter = {}
    cls_annotations = {}
    for column in User.__table__.columns._all_columns:
        parameter[user_attr[column.key]] = Field(title=user_attr[column.key])
        cls_annotations[user_attr[column.key]] = Optional[column.type.python_type]

    # parameter = {
    #     user_attr[column.key]: Field(type=column.type.python_type)
    #     for column in User.__table__.columns._all_columns
    # }

    cls = type('QAQ', (CommonBaseModel,), {'__annotations__': cls_annotations, **parameter})

    ll = cls()

    print(ll.schema())


if __name__ == '__main__':
    main()
