from pydantic import BaseModel, Field, field_validator, field_serializer, model_serializer
from typing import Optional, List, Any
import json


# --- Source Models ---

class SourceBase(BaseModel):
    type: str
    path: str
    content: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    note_id: int

    class Config:
        from_attributes = True


# --- Learning Note Models ---

class LearningNoteBase(BaseModel):
    title: str

class LearningNoteCreate(LearningNoteBase):
    pass

class LearningNote(LearningNoteBase):
    id: int
    owner_id: int
    sources: List[Source] = []
    # material: Optional['LearningMaterial'] = None # 순환 참조 방지를 위해 주석 처리 또는 ForwardRef 사용

    class Config:
        from_attributes = True


# --- MicroLearn Core Models ---

# Base models for creation
class QuizItemBase(BaseModel):
    question: str
    options: List[str]
    answer: str

class FlashcardItemBase(BaseModel):
    term: str
    definition: str

class LearningMaterialCreate(BaseModel):
    summary: str
    key_topics: List[str]
    quiz: List[QuizItemBase]
    flashcards: List[FlashcardItemBase]
    mindmap: Optional[Any] = None
    audio_url: Optional[str] = None

class SourceText(BaseModel):
    text: str

# Models for reading from DB (includes ID, etc.)
class QuizItem(QuizItemBase):
    id: int
    material_id: int

    @field_validator('options', mode='before')
    @classmethod
    def parse_options(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

    class Config:
        from_attributes = True

class FlashcardItem(FlashcardItemBase):
    id: int
    material_id: int
    class Config:
        from_attributes = True

class KeyTopic(BaseModel):
    id: int
    topic: str
    material_id: int
    class Config:
        from_attributes = True

class LearningMaterial(BaseModel):
    id: int
    summary: str
    note_id: int
    key_topics: List[KeyTopic] = []
    quiz_items: List[QuizItem] = []
    flashcards: List[FlashcardItem] = []
    mindmap: Optional[Any] = None
    audio_url: Optional[str] = None

    @field_serializer('key_topics')
    def serialize_key_topics(self, key_topics: List[KeyTopic], _info):
        return [topic.topic for topic in key_topics]

    @model_serializer(mode='wrap')
    def serialize_model(self, serializer):
        data = serializer(self)
        # Rename quiz_items to quiz for frontend compatibility
        if 'quiz_items' in data:
            data['quiz'] = data.pop('quiz_items')
        return data

    class Config:
        from_attributes = True

# 순환 참조 해결
LearningNote.model_rebuild()


# --- Auth Models ---

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    notes: List[LearningNote] = []

    class Config:
        from_attributes = True
