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
    hash: Mapped[str] = mapped_column(String(64))
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

class Movie(Base):
    """
    The table to store movies and TV shows.

    `name_original`: an original name of the movie.
    `name_russian`: a russian translation of the name.
    `duration`: the movie duration time.
    `premiere_date`: the realse year of the movie.
    `imdb_link`: a URL to IMDb page of the movie.
    `description`: some details one would like to write down.
    `active`: a boolean that answers is movie consider deleted from DB.
    `files`: a list of files linked to the movie.
    `genres`: a list of genres linked to the movie.
    """

    __tablename__ = "movie_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_original: Mapped[str] = mapped_column(String(160), nullable=True)
    name_russian: Mapped[str] = mapped_column(String(160), nullable=True)
    duration: Mapped[time] = mapped_column(Time, nullable=True)
    premiere_date: Mapped[str] = mapped_column(String(16), nullable=True)
    imdb_link: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    files: Mapped[List[File]] = relationship(back_populates="movie")

    type_id: Mapped[int] = mapped_column(ForeignKey("type_table.id"), nullable=True)
    movie_type: Mapped["Type"] = relationship( back_populates="movies")

    franchise_id: Mapped[int] = mapped_column(ForeignKey("franchise_table.id"), nullable=True)
    franchise: Mapped["Franchise"] = relationship(back_populates="movies")
    franchise_part: Mapped[int] = mapped_column(Integer, nullable=True)

    genres: Mapped[List["Genre"]] = relationship(
        secondary=genres_movies_table, back_populates="movies"
    )

    actors: Mapped[List["Person"]] = relationship(
        secondary=actors_movies_table, back_populates="movies_actors"
    )

    directors: Mapped[List["Person"]] = relationship(
        secondary=directors_movies_table, back_populates="movies_directors"
    )

