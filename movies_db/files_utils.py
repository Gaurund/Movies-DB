from hashlib import sha256
from pathlib import Path
from mimetypes import guess_file_type
from data_classes import Device, DeviceFiles, RealFile
from shutil import disk_usage
from datetime import datetime


def collect_video_files(path_str: str) -> DeviceFiles:
    """Collects video files from the specified path and returns 
    a DeviceFiles object."""
    path: Path = Path(path_str)
    total, _, free = disk_usage(path)
    device = Device(capacity=total, free=free, st_dev=str(Path(path).stat().st_dev))
    dev_files = DeviceFiles(device=device, files=[])
    for root, _, files in path.walk():
        for file in files:
            if (
                "$RECYCLE.BIN" not in str(root)
                and not guess_file_type(file)[0] == None
                and guess_file_type(file)[0].startswith("video")
            ):
                full_path = Path(root, file)
                dev_files.files.append(
                    RealFile(
                        name=file,
                        path=str(root),
                        size=full_path.stat().st_size,
                        last_mod=datetime.fromtimestamp(full_path.stat().st_mtime),
                        hash_=hash_first_64kb(full_path),
                    )
                )
    return dev_files


def hash_first_64kb(filepath) -> str:
    """Calculates the hash of the first 64KB of the file."""
    hasher = sha256()
    with open(filepath, "rb") as f:
        chunk = f.read(65536)
        hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == "__main__":
    video = collect_video_files("D:/Temp/v/")
    for file in video.files:
        print(file)

