import pyromod.listen  # noqa
import keyring
from pyrogram import Client

API_ID = keyring.get_password('session_generator_api_id', 'session_generator')
API_HASH_ID = keyring.get_password('session_generator_api_hash_id', 'session_generator')
BOT_TOKEN = keyring.get_password('session_generator_bot_token', 'session_generator')

bot = Client(
    name='session string generator',
    api_id=API_ID,
    api_hash=API_HASH_ID,
    workdir='sessions',
    plugins=dict(root='plugins'),
    bot_token=BOT_TOKEN,
)
