from typing import List
from datetime import time, datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Time,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


genres_movies_table = Table(
    "genres_movies_table",
    Base.metadata,
    Column("genre_id", ForeignKey("genre_table.id"), primary_key=True),
    Column("movie_id", ForeignKey("movie_table.id"), primary_key=True),
)


class Type(Base):
    """The table to store different types.
    `type_name`: a name of a type
    `russian_type_name`: a russian translation of the type's name
    `movies`: a list of movies with such type"""

    __tablename__ = "type_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(32))
    russian_type_name: Mapped[str] = mapped_column(String(32), nullable=True)

    movies: Mapped[List["Movie"]] = relationship(back_populates="movie_type")


class File(Base):
    """The table to store files.

    `file_name`: the name of the file.
    `disk_path`: the path to the file on disk excluding the file name.
    `hash`: the hash of the first 4KB of the file.
    `last_modified`: the last modification date of the file.
    `size`: the size of the file in bytes.
    `is_active`: a boolean that answers is file consider deleted from DB.
    `disk_id`: the foreign key to the disk table.
    `disk`: the relationship to the disk table.
    `movie_id`: the foreign key to the movie table.
    `movie`: the relationship to the movie table."""

    __tablename__ = "file_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(160))
    disk_path: Mapped[str] = mapped_column(Text)
    hash: Mapped[str] = mapped_column(String(64))
    last_modified: Mapped[datetime]
    size: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    disk_id: Mapped[int] = mapped_column(ForeignKey("disk_table.id"))
    disk: Mapped["Disk"] = relationship(back_populates="files")

    movie_id: Mapped[int] = mapped_column(ForeignKey("movie_table.id"), nullable=True)
    movie: Mapped["Movie"] = relationship(back_populates="files")


class Disk(Base):
    """The table to store disks and flash drives.

    `disk_name`: the name of the disk.
    `disk_image`: the path to the disk image if it exists.
    `disk_capacity`: the capacity of the disk in bytes.
    `disk_free`: the free space on the disk in bytes.
    `st_dev`: the device number of the disk on the system.
    `files`: a list of files linked to the disk."""

    __tablename__ = "disk_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    disk_name: Mapped[str] = mapped_column(String(30))
    disk_image: Mapped[str] = mapped_column(String(260), nullable=True)
    disk_capacity: Mapped[int] = mapped_column(BigInteger)
    disk_free: Mapped[int] = mapped_column(BigInteger)
    st_dev: Mapped[str] = mapped_column(String(32))

    files: Mapped[List[File]] = relationship(back_populates="disk")


class Genre(Base):
    """The table of genres.

    `eng_genre`: An english name of a genre
    `rus_genre`: A russian name of a genre

    `movies`: A list of movies have the genre
    """

    __tablename__ = "genre_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    eng_genre: Mapped[str] = mapped_column(String(64))
    rus_genre: Mapped[str] = mapped_column(String(64), nullable=True)

    movies: Mapped[List["Movie"]] = relationship(
        secondary=genres_movies_table, back_populates="genres"
    )

    def __repr__(self) -> str:
        return f"Genre(id={self.id}, eng_genre='{self.eng_genre}', rus_genre='{self.rus_genre}')"


class Franchise(Base):
    """The table to organize movies into franchises.

    `franchise`: a name of a franchise
    `movies`: a list of movies linked to the franchise
    """

    __tablename__ = "franchise_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    franchise: Mapped[str] = mapped_column(String(64))

    movies: Mapped[List["Movie"]] = relationship(back_populates="franchise")


class Movie(Base):
    """The table to store movies and TV shows.

    `name_original`: an original name of the movie.
    `name_russian`: a russian translation of the name.
    `duration`: the movie duration time.
    `premiere_date`: the realse year of the movie.
    `imdb_link`: a URL to IMDb page of the movie.
    `description`: some details one would like to write down.
    `active`: a boolean that answers is movie consider deleted from DB.
    `files`: a list of files linked to the movie.
    `type_id`: a foreign key to the type table.
    `movie_type`: a relationship to the type table.
    `franchise_id`: a foreign key to the franchise table.
    `franchise`: a relationship to the franchise table.
    `franchise_part`: a number of the movie in the franchise.
    `cast`: a list of people participated in the movie and their roles.
    `genres`: a list of genres linked to the movie."""

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
    movie_type: Mapped["Type"] = relationship(back_populates="movies")

    franchise_id: Mapped[int] = mapped_column(
        ForeignKey("franchise_table.id"), nullable=True
    )
    franchise: Mapped["Franchise"] = relationship(back_populates="movies")
    franchise_part: Mapped[int] = mapped_column(Integer, nullable=True)

    cast: Mapped[List["Cast"]] = relationship(back_populates="movie")

    genres: Mapped[List["Genre"]] = relationship(
        secondary=genres_movies_table, back_populates="movies", order_by="Genre.id"
    )


class Person(Base):
    """The table to store important people in the film industry.

    `full_name`: a full name of a person
    `russian_name`: a russian translation of the name
    `imdb_link`: URL to a web page of the person in IMDb
    """

    __tablename__ = "person_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(128))
    russian_name: Mapped[str] = mapped_column(String(128), nullable=True)
    imdb_link: Mapped[str] = mapped_column(String(128), nullable=True)


class Cast(Base):
    """The table to link movies, people and their roles in the movies."""

    __tablename__ = "cast"
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movie_table.id"), primary_key=True
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey("person_table.id"), primary_key=True
    )
    type_id: Mapped[int] = mapped_column(ForeignKey("type_table.id"), primary_key=True)

    movie: Mapped["Movie"] = relationship(back_populates="cast")
    person: Mapped["Person"] = relationship()
    type: Mapped["Type"] = relationship()
