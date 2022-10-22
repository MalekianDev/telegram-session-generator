from pyrogram import Client, filters
from pyrogram.types import ForceReply
from pyrogram.errors import PasswordHashInvalid, SessionPasswordNeeded
from commons.funcs import hinted_ask_str
from commons.keyboards import main_menu
from commons.texts import (CREATE_PYRO_SESSION_BTN_TEXT, GET_BOT_DETAIL_TEXT,
                           WRONG_FORMAT_TEXT, START_TEXT, GET_OPT_CODE_TEXT, GET_TWO_STEP_TEXT, WRONG_PASSWORD_TEXT)


@Client.on_message(filters.private & filters.regex(CREATE_PYRO_SESSION_BTN_TEXT))
async def pyro_session_generator_handler(_, message):
    user_chat_id = message.from_user.id
    bot_data = await hinted_ask_str(chat_id=user_chat_id, ask_text=GET_BOT_DETAIL_TEXT,
                                    hint_text=GET_BOT_DETAIL_TEXT, correct_answer_regex='.+', reply_markup=ForceReply())
    if bot_data:
        try:
            api_id, api_hash, phone_number = bot_data.split('\n')
            client = Client(name=':memory:', api_id=api_id, api_hash=api_hash, in_memory=True)
            try:
                await client.connect()
                code = await client.send_code(phone_number=phone_number)
                opt_code = await hinted_ask_str(chat_id=user_chat_id, ask_text=GET_OPT_CODE_TEXT,
                                                hint_text=GET_OPT_CODE_TEXT, correct_answer_regex=r'^\d{5}$',
                                                reply_markup=ForceReply())
                if opt_code:
                    try:
                        await client.sign_in(phone_number=phone_number,
                                             phone_code_hash=code.phone_code_hash, phone_code=opt_code)
                    except SessionPasswordNeeded:
                        password = await hinted_ask_str(chat_id=user_chat_id, ask_text=GET_TWO_STEP_TEXT,
                                                        hint_text=GET_TWO_STEP_TEXT, correct_answer_regex=r'.+',
                                                        reply_markup=ForceReply())
                        try:
                            await client.check_password(password)
                            string_session = await client.export_session_string()
                            await message.reply(string_session, reply_markup=main_menu)
                        except PasswordHashInvalid:
                            await message.reply(WRONG_PASSWORD_TEXT, reply_markup=main_menu)
                else:
                    await message.reply(START_TEXT, reply_markup=main_menu)
            except Exception as e:
                await message.reply(str(e), reply_markup=main_menu)
            await client.disconnect()
        except ValueError:
            await message.reply(WRONG_FORMAT_TEXT, reply_markup=main_menu)
    else:
        await message.reply(START_TEXT, reply_markup=main_menu)
