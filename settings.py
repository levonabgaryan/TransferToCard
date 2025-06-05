import os
from typing import Final
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DOMAIN: Final[str] = os.environ.get('DOMAIN')
PARTNER_ID: Final[int] = int(os.environ.get('PARTNER_ID'))
SIGNATURE: Final[str] = os.environ.get('SIGNATURE')
