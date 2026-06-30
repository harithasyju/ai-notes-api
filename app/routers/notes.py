from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.ai_service import summarize_note
from typing import List
router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
        owner=current_user,
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note
@router.get("/", response_model=List[NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notes = db.query(Note).filter(Note.owner_id == current_user.id).all()
    return notes

def get_user_note_or_404(note_id: str, db: Session, current_user: User):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to access this note")

    return note
@router.get("/{note_id}", response_model=NoteResponse)

def get_note(note_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_note_or_404(note_id, db, current_user)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: str,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = get_user_note_or_404(note_id, db, current_user)

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = get_user_note_or_404(note_id, db, current_user)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this note")

    db.delete(note)
    db.commit()

    return None
@router.post("/{note_id}/summarize", response_model=NoteResponse)
def summarize_user_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = get_user_note_or_404(note_id, db, current_user)

    if note.summary:
        return note

    summary = summarize_note(
        title=note.title,
        content=note.content,
    )

    note.summary = summary

    db.commit()
    db.refresh(note)

    return note