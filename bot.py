import asyncio
from config import *
import requests
import os
import random
from aiogram import Bot, Dispatcher, executor, types, filters

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(filters.CommandStart())
async def start(message):
    await message.answer("Assalomu alaykum.\nMenga biron bir rasm jo'nating")

@dp.message_handler(content_types=["text", "document"])
async def undefined_text(message):
    await message.reply("Menga biron bir rasm jo'nating.")

@dp.message_handler(content_types=["photo"])
async def photo(message):
    if os.path.exists(f"{message.from_user.id}.jpg"): os.remove(f"{message.from_user.id}.jpg")
    await message.photo[-1].download(f"./{message.from_user.id}.jpg")
    await message.reply(f"Yuklab oldim")
    API = random.choice(API_KEYS)
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(f"./{message.from_user.id}.jpg", 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': API},
    )
    if response.status_code == requests.codes.ok:
        f = f"no-bg{message.from_user.id}.png"
        if os.path.exists(f): os.remove(f)
        out = open(f, 'wb')
        out.write(response.content)
        await message.reply_document(open(f, 'rb'), caption="Tayyor akasi")
    else:
        print("Error:", response.status_code, response.text)
        await message.reply(f"Error bo'ldiku akasi.\n\nError: {response.status_code} {response.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
