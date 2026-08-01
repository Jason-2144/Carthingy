import pytest

def test_password_strength_validation():
    from backend.operations.authentication.security import validate_password_strength
    assert not validate_password_strength("weak")
    assert not validate_password_strength("NoSpecialChar123")
    assert not validate_password_strength("NoNumber!!!")
    assert validate_password_strength("StrongPass123!")

def test_jwt_generation():
    from backend.operations.authentication.security import create_access_token
    token = create_access_token("user-123")
    assert isinstance(token, str)
    assert len(token) > 0
