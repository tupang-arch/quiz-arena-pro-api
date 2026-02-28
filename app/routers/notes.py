from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_db, get_current_user
from ..models import Note, User
from ..schemas import NoteCreate, NoteOut

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteOut)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_note = Note(title=note.title, owner_id=user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=list[NoteOut])
def get_my_notes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.query(Note).filter(Note.owner_id == user.id).all()