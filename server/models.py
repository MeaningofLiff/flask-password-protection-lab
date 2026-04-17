#!/usr/bin/env python3

from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    # hide password
    @hybrid_property
    def password_hash(self):
        raise Exception("Password hashes may not be viewed.")

    # hash password
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    # authenticate
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode("utf-8")
        )

    # replace SerializerMixin
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        } 