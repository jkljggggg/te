import os
import time

import requests
from pyrogram.types import Message

from Pbxbot.core import ENV
from Pbxbot.functions.formatter import readable_time
from Pbxbot.functions.images import get_wallpapers, make_logo

from . import Config, HelpMenu, db, Pbxbot, on_message


@on_message("logo", allow_stan=True)
async def makeLogo(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a text to make a logo.")

    start_time = time.time()
    Pbx = await Pbxbot.edit(message, "Processing...")
    query = await Pbxbot.input(message)

    if message.reply_to_message and message.reply_to_message.photo:
        photo = await message.reply_to_message.download(Config.TEMP_DIR + "temp_bg.jpg")
        text = query
    else:
        if "--" in query:
            text, theme = query.split("--", 1)
            isRandom = False
        else:
            text, theme = query, ""
            isRandom = True

        access = await db.get_env(ENV.unsplash_api)
        if not access:
            return await Pbxbot.delete(
                Pbx, "Unsplash API not found. Either set it or reply to an image."
            )

        photo = await get_wallpapers(access, 1, theme.strip(), isRandom)
        if not photo:
            return await Pbxbot.delete(Pbx, "No wallpapers found.")

        binary = requests.get(photo[0]).content
        with open(Config.TEMP_DIR + "temp_bg.jpg", "wb") as f:
            f.write(binary)

    logo_path = await make_logo(Config.TEMP_DIR + "temp_bg.jpg", text.strip(), Config.FONT_PATH)
    time_taken = readable_time(int(time.time() - start_time))

    await message.reply_photo(
        logo_path,
        caption=f"**𝖫𝗈𝗀𝗈 𝖬𝖺𝖽𝖾 𝗂𝗇:** `{time_taken}`",
    )
    await Pbx.delete()
    os.remove(logo_path)


@on_message("setfont", allow_stan=True)
async def setFont(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await Pbxbot.delete(message, "Reply to a font file to save it.")

    Pbx = await Pbxbot.edit(message, "Processing...")
    font = await message.reply_to_message.download(Config.DWL_DIR)

    if not font.endswith(".ttf"):
        return await Pbxbot.delete(Pbx, "Invalid font file. Only .ttf is supported.")

    if not os.path.exists(font):
        return await Pbxbot.delete(Pbx, "Font not found.")

    Config.FONT_PATH = font
    await Pbxbot.delete(Pbx, "Font set successfully.")


@on_message("resetfont", allow_stan=True)
async def resetFont(_, message: Message):
    prev_font = Config.FONT_PATH
    if prev_font == "./Pbxbot/resources/fonts/Montserrat.ttf":
        return await Pbxbot.delete(message, "Font is already set to default.")

    Config.FONT_PATH = "./Pbxbot/resources/fonts/Montserrat.ttf"
    await Pbxbot.delete(message, "Font reset successfully.")
    os.remove(prev_font)


HelpMenu("logo").add(
    "logo",
    "<reply to image (optional)> <text>",
    "Make a logo with text. You can also reply to an image to use it as a background. You can also specify a theme by using `--` after the text.",
    "logo Badhacker98 --supra",
    "This command uses Unsplash API to get images.",
).add(
    "setfont",
    "<reply to font file>",
    "Set a font file to use for logo making. This is not permanent option.",
    "setfont",
    "Only .ttf files are supported.",
).add(
    "resetfont",
    None,
    "Reset the font file to default.",
    "resetfont",
).info(
    "Make Logos"
).done()
