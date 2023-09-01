#!/usr/bin/env python3
"""Encrypting passwords and checking validity"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ perform the hashing (with hashpw)."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check valid password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
