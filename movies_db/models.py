from typing import List
from datetime import time, datetime
from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class File(Base):
    __tablename__ = "file_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(160))
    disk_path: Mapped[str] = mapped_column(Text)
    st_ino: Mapped[str] = mapped_column(String(28))
    last_modified: Mapped[datetime]
    size: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    disk_id: Mapped[int] = mapped_column(ForeignKey("disk_table.id"))
    disk: Mapped["Disk"] = relationship(back_populates="files")

    # movie_id: Mapped[int] = mapped_column(ForeignKey("movie_table.id"), nullable=True)
    # movie: Mapped["Movie"] = relationship(back_populates="files")


class Disk(Base):
    __tablename__ = "disk_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    disk_name: Mapped[str] = mapped_column(String(30))
    disk_image: Mapped[str] = mapped_column(String(260), nullable=True)
    disk_capacity: Mapped[int] = mapped_column(BigInteger)
    disk_free: Mapped[int] = mapped_column(BigInteger)
    st_dev: Mapped[str] = mapped_column(String(32))

    files: Mapped[List[File]] = relationship(back_populates="disk")
