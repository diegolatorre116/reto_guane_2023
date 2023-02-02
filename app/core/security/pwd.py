from passlib.context import CryptContext

# Handles the passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Functions to encrypt passwords and to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password):
    return pwd_context.hash(password)