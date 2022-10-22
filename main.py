from pyrogram import filters
from configs import bot
from commons.texts import START_TEXT
from commons.keyboards import main_menu


@bot.on_message(filters.private & filters.command(['start', 'cancel']))
async def start_handler(_, message):
    await message.reply(START_TEXT, reply_markup=main_menu)


if __name__ == '__main__':
    bot.run()
