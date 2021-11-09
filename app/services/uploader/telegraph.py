import asyncio
import json
import os
import secrets
from pathlib import Path
from typing import List

import aiohttp

from app.services.uploader.exceptions import NoFilesPassed


def _guess_filename(obj):
    name = getattr(obj, 'name', None)
    if name and isinstance(name, str) and name[0] != '<' and name[-1] != '>':
        return os.path.basename(name)


async def upload_to_telegraph(*files, full=True) -> List[str]:
    to_be_closed = []
    form = aiohttp.FormData(quote_fields=False)
    try:
        for file in files:
            if isinstance(file, tuple):
                if len(file) == 2:
                    filename, fileobj = file
                    content_type = None
                elif len(file) == 3:
                    filename, fileobj, content_type = file
                else:
                    raise ValueError('Tuple must have exactly 2 or 3 elements: filename, fileobj, content_type')
            elif isinstance(file, (str, Path)):
                fileobj = open(file, 'rb')
                to_be_closed.append(fileobj)
                filename = os.path.basename(file)
                content_type = None
            else:
                fileobj = file
                filename = _guess_filename(file)
                content_type = None

            form.add_field(secrets.token_urlsafe(8), fileobj, filename=filename, content_type=content_type)

        async with aiohttp.ClientSession() as session:
            async with session.post('https://telegra.ph/upload', data=form) as response:
                result = await response.json(loads=json.loads)
    finally:
        for item in to_be_closed:
            item.close()

    if isinstance(result, dict) and 'error' in result:
        raise NoFilesPassed()

    if full:
        return ['https://telegra.ph' + item['src'] for item in result if 'src' in item]
    return [item['src'] for item in result if 'src' in item]
