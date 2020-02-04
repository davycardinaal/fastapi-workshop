from datetime import datetime, timezone
from typing import Optional

import pytz
import sqlalchemy
from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Dialect
from sqlalchemy.exc import DontWrapMixin
from sqlalchemy.orm import backref, relationship


class UtcTimestampException(Exception, DontWrapMixin):
    pass


class UtcTimestamp(TypeDecorator):
    """Timestamps in UTC.

    This column type always returns timestamps with the UTC timezone, regardless of the database/connection time zone
    configuration. It also guards against accidentally trying to store Python naive timestamps (those without a time
    zone).
    """

    impl = sqlalchemy.types.TIMESTAMP(timezone=True)

    def process_bind_param(self, value: Optional[datetime], dialect: Dialect) -> Optional[datetime]:
        if value is not None:
            if value.tzinfo is None:
                raise UtcTimestampException(f"Expected timestamp with tzinfo. Got naive timestamp {value!r} instead")
        return value

    def process_result_value(self, value: Optional[datetime], dialect: Dialect) -> Optional[datetime]:
        if value is not None:
            return value.astimezone(timezone.utc)
        return value


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(UtcTimestamp, default=datetime.now(tz=pytz.utc))
    is_active = Column(Boolean, default=True)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(60), unique=True, index=True)

    def __repr__(self):
        return self.name


class Todo(Base):
    __tablename__ = 'todo_items'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(60), unique=True, index=True)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(UtcTimestamp, default=datetime.now(tz=pytz.utc))
    created_by = Column('created_by', UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    todo_tags = relationship("Tag", secondary='todo_tags')
    todo_to_tags = relationship("TodoTag")

    def __repr__(self):
        return self.name


class TodoTag(Base):
    __tablename__ = 'todo_tags'
    id = Column(UUID(as_uuid=True), primary_key=True)
    todo_id = Column('todo_id', UUID(as_uuid=True), ForeignKey('todo_items.id'), index=True)
    tag_id = Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), index=True)
    todo = relationship("Todo", lazy=True)
    tag = relationship("Tag", lazy=True)

    def __repr__(self):
        return self.tag.name
