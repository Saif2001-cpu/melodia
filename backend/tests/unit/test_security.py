"""Unit tests for core security utilities."""

import pytest

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

settings = get_settings()


class TestPasswordHashing:
    def test_hash_and_verify(self):
        plain = "super-secret-pw-123"
        hashed = hash_password(plain)
        assert verify_password(plain, hashed)

    def test_wrong_password_fails(self):
        hashed = hash_password("correct")
        assert not verify_password("wrong", hashed)

    def test_hashes_differ(self):
        """bcrypt salts must produce different hashes each call."""
        pw = "same-password"
        assert hash_password(pw) != hash_password(pw)


class TestJWT:
    def test_access_token_roundtrip(self):
        user_id = "user-abc-123"
        token = create_access_token(user_id)
        assert decode_token(token) == user_id

    def test_refresh_token_roundtrip(self):
        user_id = "user-xyz-456"
        token = create_refresh_token(user_id)
        assert decode_token(token, expected_type="refresh") == user_id

    def test_wrong_token_type_raises(self):
        token = create_refresh_token("user-1")
        with pytest.raises(UnauthorizedError):
            decode_token(token, expected_type="access")

    def test_invalid_token_raises(self):
        with pytest.raises(UnauthorizedError):
            decode_token("not.a.valid.jwt")

    def test_tampered_token_raises(self):
        token = create_access_token("user-1")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(UnauthorizedError):
            decode_token(tampered)
