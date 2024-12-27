from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from . import db

def get_uuid_str() -> str:
    return str(uuid.uuid4())

user_file_access = db.Table(
    'user_file_access',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
    db.Column('file_uuid', db.String, db.ForeignKey('file.uuid'), index=True)
)


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(120), unique=True,
                                          nullable=False, index=True)
    email: Mapped[str] = mapped_column(db.String(120), unique=True,
                                       nullable=False)
    password: Mapped[str] = mapped_column(db.String(60), nullable=False)
    files: Mapped[list['File']] = relationship('File', backref='owner',
                                               lazy=True)

    def __repr__(self) -> str:
        return f'<User id={self.id} username={self.username}>'


class File(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=get_uuid_str)
    filename: Mapped[str] = mapped_column(db.String(250), nullable=False)
    owner_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'),
                                          nullable=False)
    extension: Mapped[str] = mapped_column(db.String(10), nullable=False)
    access_users: Mapped[list['User']] = relationship('User',
                                                      secondary=user_file_access,
                                                      backref='access_files',
                                                      lazy=True)

    def __repr__(self) -> str:
        return f'<File id={self.id} filename={self.filename}>'
