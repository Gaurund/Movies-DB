from datetime import datetime
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from movies_db.models import Base, Disk, File


class TestDiskModel(TestCase):
    def setUp(self):
        # Create database connection and tables if necessary
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        disk = Disk(
            id=1,
            disk_name="Test Disk",
            disk_image="/path/to/disk/image",
            disk_capacity=1000000000,
            disk_free=500000000,
            st_dev="sda1",
        )
        self.session.add(disk)
        self.session.commit()
        file = File(
            id=1,
            file_name="test_file.mkv",
            disk_path="/path/to/disk/image",
            st_ino="12345",
            last_modified=datetime(2024, 6, 1, 12, 0, 0),
            size=1000000,
            is_active=True,
            disk_id=1,
        )
        self.session.add(file)
        self.session.commit()
        self.disk = self.session.get(Disk, 1)
        self.file = self.session.get(File, 1)
        self.none_disk = self.session.get(Disk, 0)

    def tearDown(self):
        # Clean up database connection
        self.session.close()

    def test_disk_model_creation(self):
        self.assertEqual(self.disk.id, 1)
        self.assertEqual(self.disk.disk_name, "Test Disk")
        self.assertEqual(self.disk.disk_image, "/path/to/disk/image")
        self.assertEqual(self.disk.disk_capacity, 1000000000)
        self.assertEqual(self.disk.disk_free, 500000000)
        self.assertEqual(self.disk.st_dev, "sda1")
        self.assertIsNone(self.none_disk)

    def test_file_model_creation(self):
        self.assertEqual(self.file.id, 1)
        self.assertEqual(self.file.file_name, "test_file.mkv")
        self.assertEqual(self.file.disk_path, "/path/to/disk/image")
        self.assertEqual(self.file.st_ino, "12345")
        self.assertEqual(self.file.last_modified, datetime(2024, 6, 1, 12, 0, 0))
        self.assertEqual(self.file.size, 1000000)
        self.assertTrue(self.file.is_active)
        self.assertEqual(self.file.disk_id, 1)