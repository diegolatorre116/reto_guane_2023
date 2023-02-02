from fastapi import HTTPException, Depends, status
from jose import JWTError, jwt

from app.schemas import TokenData
from app.config import settings
from app.core.security.token import oauth2_scheme
from app.core.security.pwd import verify_password
from app.internal.user_crud import user

async def authenticate_user(username:str, password:str):
        user_to_authenticate = await user.get_by_field(
            field="username",
            value=username
            ) 
        if not user_to_authenticate:
            return False
        if not verify_password(password, user_to_authenticate['password']):
            return False
        return user_to_authenticate

async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
                )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        current_user = await user.get_by_field(
            field="username",
            value=token_data.username
            )
        if current_user is None:
            raise credentials_exception
        return current_user


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#         credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#         payload = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=[settings.ALGORITHM]
#                 )
#         username: str = payload.get("sub")
#         token_data = TokenData(username=username)
#         current_user = await user.get_by_field(
#             field="username",
#             value=token_data.username
#             )
#         print(current_user)
#         return current_user