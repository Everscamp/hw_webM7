from sqlalchemy import String, ForeignKey
import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship)
from connect_db import Base

class Tutor(Base):
    __tablename__ = "tutors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    subject: Mapped[list["Subject"]] = relationship(
        back_populates="tutor",
        cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Tunor({self.name})"


class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    
    tutor: Mapped["Tutor"] = relationship(
        back_populates="subject")

    mark: Mapped["Marks"] = relationship(
        backref="subject", uselist=False)
    
    def __repr__(self) -> str:
        return self.name

class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    student: Mapped[list["Student"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return self.name


class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    
    group: Mapped["Group"] = relationship(
        back_populates="student")

    mark: Mapped["Marks"] = relationship(
        backref="student", uselist=False)
    
    def __repr__(self) -> str:
        return self.name

class Marks(Base):
    __tablename__ = "marks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[int] = mapped_column(Integer)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    date: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"Mark({self.mark})"
    
    

if __name__ == '__main__':
    ...