import sqlalchemy as schema
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import BOOLEAN, VARCHAR, BIGINT, TIMESTAMP, JSONB

from core.app.extensions import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'

    id = schema.Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    telegram_id = schema.Column(BIGINT, unique=True)
    name = schema.Column(VARCHAR(128))
    last_name = schema.Column(VARCHAR(128))
    phone = schema.Column(VARCHAR(16), unique=True)
    email = schema.Column(VARCHAR(128))
    password = schema.Column(VARCHAR(128))
    settings = schema.Column(JSONB, server_default='{}', default={})
    nickname = schema.Column(VARCHAR(128))
    created_at = schema.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = schema.Column(TIMESTAMP(timezone=True), onupdate=func.now())
    enabled = schema.Column(BOOLEAN, server_default='true')

    def __init__(self, telegram_id=None, name=None, phone=None, email=None, password=None, last_name=None,
                 settings='{}', nickname=None, enabled=None):
        self.telegram_id = telegram_id
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.settings = settings
        self.nickname = nickname
        self.enabled = enabled
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @classmethod
    def from_dict(cls, adict):
        user = User(
            telegram_id=adict['telegram_id'] if 'telegram_id' in adict else None,
            name=adict['name'] if 'name' in adict else None,
            last_name=adict['last_name'] if 'last_name' in adict else None,
            phone=adict['phone'] if 'phone' in adict else None,
            email=adict['email'] if 'email' in adict else None,
            settings=adict['settings'] if 'settings' in adict else '{}',
            nickname=adict['nickname'] if 'nickname' in adict else None,
            enabled=adict['enabled'] if 'enabled' in adict else True,
            password=adict['password'] if 'password' in adict else None,
        )
        return user

    def to_dict(self):
        return {
            'telegram_id': self.telegram_id,
            'name': self.name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'settings': self.settings,
            'nickname': self.nickname,
            'enabled': self.enabled,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return '{}'.format(self.id)
