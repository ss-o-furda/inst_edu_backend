import os

import aiofiles
from fastapi import UploadFile


async def write_new_file(file_location: str, file: UploadFile) -> None:
    async with aiofiles.open(file_location, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk


def get_file_ext(file: UploadFile):
    _, file_ext = os.path.splitext(file.filename)
    return file_ext
