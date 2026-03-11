from datetime import datetime, time
from unittest import TestCase

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload
from movies_db.models import Base, Disk, File, Franchise, Movie, Person, Type


class TestModels(TestCase):

    def setUp(self):
        # Create database connection and tables
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            disk = Disk(
                id=1,
                disk_name="Test Disk",
                disk_image="/path/to/disk/image",
                disk_capacity=1000000000,
                disk_free=500000000,
                st_dev="sda1",
            )
            session.add(disk)
            file1 = File(
                id=1,
                file_name="test_file.mkv",
                disk_path="/path/to/disk/image",
                st_ino="12345",
                hash="abcdef1234567890",
                last_modified=datetime(2024, 6, 1, 12, 0, 0),
                size=1000000,
                is_active=True,
                disk_id=1,
                movie_id=1,
            )
            session.add(file1)
            file2 = File(
                id=2,
                file_name="test_file_2.mkv",
                disk_path="/path/to/disk/image",
                st_ino="12350",
                hash="abcdef1234567890",
                last_modified=datetime(2020, 5, 1, 11, 0, 0),
                size=1000000,
                is_active=True,
                disk_id=1,
                movie_id=1,
            )
            session.add(file2)
            type1 = Type(id=1, type_name="Test Type", russian_type_name="Тестовый тип")
            session.add(type1)
            type2 = Type(
                id=2, type_name="Test Type 2", russian_type_name="Тестовый тип 2"
            )
            session.add(type2)
            franchise1 = Franchise(
                id=1,
                franchise="Test Franchise",
            )
            session.add(franchise1)
            movie1 = Movie(
                id=1,
                name_original="Test Movie",
                name_russian="Тестовый фильм",
                duration=time(2, 0, 0),
                premiere_date="2024",
                imdb_link="https://www.imdb.com/title/tt0000000/",
                description="A test movie for unit testing.",
                type_id=1,
            )
            session.add(movie1)
            movie2 = Movie(
                id=2,
                name_original="Test Movie 2",
                name_russian="Тестовый фильм 2",
                duration=time(2, 0, 0),
                premiere_date="2024",
                imdb_link="https://www.imdb.com/title/tt0000001/",
                description="A test movie for unit testing.",
                type_id=1,
                franchise_id=1,
                franchise_part=2,
            )
            session.add(movie2)

            person1 = Person(
                id=1, full_name="Test Actor", russian_name="Тестовый актер"
            )
            session.add(person1)
            session.commit()
            self.disk = session.scalars(
                select(Disk).options(selectinload(Disk.files)).where(Disk.id == 1)
            ).first()
            self.file = session.get(File, 1)
            self.none_disk = session.get(Disk, 0)
            self.movie = session.scalars(
                select(Movie)
                .options(selectinload(Movie.files), selectinload(Movie.movie_type))
                .where(Movie.id == 1)
            ).first()
            self.franchise = session.get(Franchise, 1)
            self.fr_movies = session.scalars(
                select(Movie).where(Movie.franchise_id != None)
            ).all()
            self.type = session.scalars(
                select(Type).options(selectinload(Type.movies)).where(Type.id == 1)
            ).first()
            self.person1 = session.get(Person, 1)

    def tearDown(self):
        # Close database connection
        self.engine.dispose()

    def test_disk_model_creation(self):
        self.assertEqual(self.disk.id, 1)
        self.assertEqual(self.disk.disk_name, "Test Disk")
        self.assertEqual(self.disk.disk_image, "/path/to/disk/image")
        self.assertEqual(self.disk.disk_capacity, 1000000000)
        self.assertEqual(self.disk.disk_free, 500000000)
        self.assertEqual(self.disk.st_dev, "sda1")
        self.assertIsNone(self.none_disk)
        self.assertEqual(len(self.disk.files), 2)
        self.assertEqual(self.disk.files[0].file_name, "test_file.mkv")
        self.assertEqual(self.disk.files[1].file_name, "test_file_2.mkv")

    def test_file_model_creation(self):
        self.assertEqual(self.file.id, 1)
        self.assertEqual(self.file.file_name, "test_file.mkv")
        self.assertEqual(self.file.disk_path, "/path/to/disk/image")
        self.assertEqual(self.file.st_ino, "12345")
        self.assertEqual(self.file.hash, "abcdef1234567890")
        self.assertEqual(self.file.last_modified, datetime(2024, 6, 1, 12, 0, 0))
        self.assertEqual(self.file.size, 1000000)
        self.assertTrue(self.file.is_active)
        self.assertEqual(self.file.disk_id, 1)

    def test_movie_model_creation(self):
        self.assertEqual(self.movie.id, 1)
        self.assertEqual(self.movie.name_original, "Test Movie")
        self.assertEqual(self.movie.name_russian, "Тестовый фильм")
        self.assertEqual(self.movie.duration, time(2, 0, 0))
        self.assertEqual(self.movie.premiere_date, "2024")
        self.assertEqual(self.movie.imdb_link, "https://www.imdb.com/title/tt0000000/")
        self.assertEqual(self.movie.description, "A test movie for unit testing.")
        self.assertTrue(self.movie.is_active)
        self.assertEqual(len(self.movie.files), 2)
        self.assertEqual(self.movie.files[0].file_name, "test_file.mkv")
        self.assertEqual(self.movie.files[1].file_name, "test_file_2.mkv")
        self.assertEqual(self.movie.type_id, 1)
        self.assertEqual(self.movie.movie_type.type_name, "Test Type")

    def test_type_model_creation(self):
        self.assertEqual(self.type.id, 1)
        self.assertEqual(self.type.type_name, "Test Type")
        self.assertEqual(self.type.russian_type_name, "Тестовый тип")
        self.assertEqual(len(self.type.movies), 2)
        self.assertEqual(self.type.movies[0].name_original, "Test Movie")
        self.assertEqual(self.type.movies[1].name_original, "Test Movie 2")

    def test_person_model_creation(self):
        self.assertEqual(self.person1.id, 1)
        self.assertEqual(self.person1.full_name, "Test Actor")
        self.assertEqual(self.person1.russian_name, "Тестовый актер")

    def test_franchise_model_creation(self):
        self.assertEqual(self.franchise.id, 1)
        self.assertEqual(self.franchise.franchise, "Test Franchise")
        self.assertEqual(len(self.fr_movies), 1)
        self.assertEqual(self.fr_movies[0].name_original, "Test Movie 2")