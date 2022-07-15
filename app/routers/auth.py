from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2
from ..database import get_db
from ..utils.password import verify_password

router = APIRouter()

@router.post('/login')
def login(login: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='E-mail address does not exist!')
    
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect password!')
    
    access_token = oauth2.create_access_token(data = { 'user_id': user.id })

    return { 'access_token': access_token, 'token_type': 'bearer' }