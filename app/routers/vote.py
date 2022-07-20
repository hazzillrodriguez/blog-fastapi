from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(tags=['Votes'])

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: { vote.post_id } does not exist!')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    if vote.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail=f'User id: { current_user.id } has already voted post id: { vote.post_id }!')
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return { 'message': 'Successfully voted!' }
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail='Vote does not exist!')
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return { 'message': 'Vote has been deleted!' }