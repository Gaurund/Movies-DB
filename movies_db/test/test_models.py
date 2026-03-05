from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from movies_db.models import Base, Disk


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
        self.disk = self.session.get(Disk, 1)
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
        print("Disk model creation test passed.")
