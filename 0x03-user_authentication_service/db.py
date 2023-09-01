#!/usr/bin/env python3
"""DB module

contains the class DB definition of functions and methods
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


VALID = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """
    A Database class for managing user data.
    This class provides methods for initializing the database,
    adding users, and managing database sessions.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        Initializes the database engine, drops existing tables,
        creates new tables,and initializes a session
        for database operations.
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        get a session object for database operations.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        if not email or not hashed_password:
            raise ValueError("Both email and hashed_password are required.")
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ returns the first row found in the users table"""
        if not kwargs or any(field not in VALID for field in kwargs):
            raise InvalidRequestError
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates user details in database"""
        user = self.find_user_by(id=user_id)
        for i, j in kwargs.items():
            if i not in VALID:
                raise ValueError
            setattr(user, i, j)
        self._session.commit()
