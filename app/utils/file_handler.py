import os
import shortuuid

def save_upload(file):
    ext = file.filename.split('.')[-1]
    fname = f"{shortuuid.uuid()}.{ext}"
    path = os.path.join("app/storage", fname)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path