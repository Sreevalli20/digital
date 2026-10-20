"""
Patient domain model.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    UNKNOWN = 'unknown'


@dataclass
class Patient:
    """Represents a patient in the Digital Twin system."""
    
    id: Optional[int] = None
    external_id: Optional[str] = None
    first_name: str = ''
    last_name: str = ''
    date_of_birth: Optional[datetime] = None
    gender: Gender = Gender.UNKNOWN
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_synthetic: bool = False
    
    @property
    def full_name(self) -> str:
        """Return the patient's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or "Unknown Patient"
    
    @property
    def age(self) -> Optional[int]:
        """Calculate age from date of birth."""
        if not self.date_of_birth:
            return None
        today = datetime.utcnow()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return max(0, years)
    
    def to_dict(self) -> dict:
        """Convert patient to dictionary representation."""
        return {
            'id': self.id,
            'external_id': self.external_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender.value if self.gender else None,
            'age': self.age,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_synthetic': self.is_synthetic
        }
