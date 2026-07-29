from app.user.services.password import hash_password, verify_password


def test_hash_password_does_not_store_plain_value():
    password = "senha-segura-123"
    stored = hash_password(password)

    assert stored != password
    assert stored.startswith("scrypt$")
    assert verify_password(password, stored) == (True, False)


def test_legacy_plain_password_is_accepted_once_and_requires_rehash():
    assert verify_password("senha-legada", "senha-legada") == (True, True)
    assert verify_password("senha-incorreta", "senha-legada") == (False, True)
