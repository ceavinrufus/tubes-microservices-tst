from fastapi import Depends, Security, Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.middleware.authentication import AuthHandler

auth = AuthHandler()

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:  bool = True, roles: list = None):
        super().__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Scheme Invalid")
            decoded = auth.get_current_user(credentials.credentials)
            if decoded is not None:
                if self.roles and decoded.role not in self.roles:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Unauthorized: Invalid role')
                return decoded
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    