import os
import time

import requests
from lyricsgenius import Genius
from pyrogram import Client
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message
from yt_dlp import YoutubeDL

from Pbxbot.core import ENV
from Pbxbot.functions.driver import YoutubeDriver
from Pbxbot.functions.paste import post_to_telegraph
from Pbxbot.functions.tools import progress

from . import HelpMenu, Symbols, db, Pbxbot, on_message

# Path to the cookies file
COOKIES_FILE_PATH = "cookies.txt"

@on_message("song", allow_stan=True)
async def dwlSong(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to download.")

    query = await Pbxbot.input(message)
    Pbx = await Pbxbot.edit(message, f"🔎 __𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀__ `{query}`...")

    ytSearch = YoutubeDriver(query, 1).to_dict()[0]
    upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖲𝗈𝗇𝗀 ...** \n\n**{Symbols.anchor} 𝖳𝗂𝗍𝗅𝖾:** `{ytSearch['title'][:50]}`\n**{Symbols.anchor} 𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{ytSearch['channel']}`\n**{Symbols.anchor} 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{ytSearch['duration']}`"

    try:
        url = f"https://www.youtube.com{ytSearch['url_suffix']}"
        ydl_opts = {
            'cookiefile': COOKIES_FILE_PATH,
            **YoutubeDriver.song_options(),
        }
        with YoutubeDL(ydl_opts) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)

        await Pbx.edit(upload_text)
        resp = requests.get(ytSearch["thumbnail"])
        with open(f"{yt_file}.jpg", "wb") as thumbnail:
            thumbnail.write(resp.content)

        start_time = time.time()
        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {ytSearch['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{ytSearch['views']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{ytSearch['duration']}`",
            duration=int(yt_data["duration"]),
            performer="[ᴛʜᴇ ᴘʙx 2.0]",
            title=ytSearch["title"],
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                Pbx,
                start_time,
                upload_text,
            ),
        )
        await Pbx.delete()
    except Exception as e:
        return await Pbxbot.delete(Pbx, f"**🍀 𝖲𝗈𝗇𝗀 𝖭𝗈𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝖾𝖽:** `{e}`")

    try:
        os.remove(f"{yt_file}.mp3")
        os.remove(f"{yt_file}.jpg")
    except:
        pass


@on_message("video", allow_stan=True)
async def dwlVideo(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to download.")

    query = await Pbxbot.input(message)
    Pbx = await Pbxbot.edit(message, f"🔎 __𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖵𝗂𝖽𝖾𝗈 𝖲𝗈𝗇𝗀__ `{query}`...")

    ytSearch = YoutubeDriver(query, 1).to_dict()[0]
    upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖵𝗂𝖽𝖾𝗈 𝖲𝗈𝗇𝗀 ...** \n\n**{Symbols.anchor} 𝖳𝗂𝗍𝗅𝖾:** `{ytSearch['title'][:50]}`\n**{Symbols.anchor} 𝖢𝗁𝖺𝗇𝗇𝖾𝗅:** `{ytSearch['channel']}`\n**{Symbols.anchor} 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{ytSearch['duration']}`"

    try:
        url = f"https://www.youtube.com{ytSearch['url_suffix']}"
        ydl_opts = {
            'cookiefile': COOKIES_FILE_PATH,
            **YoutubeDriver.video_options(),
        }
        with YoutubeDL(ydl_opts) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        await Pbx.edit(upload_text)
        resp = requests.get(ytSearch["thumbnail"])
        with open(f"{yt_file}.jpg", "wb") as thumbnail:
            thumbnail.write(resp.content)

        start_time = time.time()
        await message.reply_video(
            f"{yt_file}.mp4",
            caption=f"**🎧 𝖳𝗂𝗍𝗅𝖾:** {ytSearch['title']} \n\n**👀 𝖵𝗂𝖾𝗐𝗌:** `{ytSearch['views']}` \n**⌛ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{ytSearch['duration']}`",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                Pbx,
                start_time,
                upload_text,
            ),
        )
        await Pbx.delete()
    except Exception as e:
        return await Pbxbot.delete(Pbx, f"**🍀 𝖵𝗂𝖽𝗂𝗈 𝖲𝗈𝗇𝗀 𝖭𝗈𝗍 𝖣𝗈𝗐𝗓𝗇𝗅𝗈𝖺𝖽𝖾𝖽:** `{e}`")

    try:
        os.remove(f"{yt_file}.mp4")
        os.remove(f"{yt_file}.jpg")
    except:
        pass


@on_message("lyrics", allow_stan=True)
async def getlyrics(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to fetch lyrics.")

    api = await db.get_env(ENV.lyrics_api)
    if not api:
        return await Pbxbot.delete(message, "Lyrics API not found.")

    query = await Pbxbot.input(message)
    if "-" in query:
        artist, song = query.split("-")
    else:
        artist, song = "", query

    Pbx = await Pbxbot.edit(message, f"🔎 __𝖫𝗒𝗋𝗂𝖼𝗌 𝖲𝗈𝗇𝗀__ `{query}`...")

    genius = Genius(
        api,
        verbose=False,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
    )

    song = genius.search_song(song, artist)
    if not song:
        return await Pbxbot.delete(Pbx, "No results found.")

    title = song.full_title
    image = song.song_art_image_url
    artist = song.artist
    lyrics = song.lyrics

    outStr = f"<b>{Symbols.anchor} Title:</b> <code>{title}</code>\n<b>{Symbols.anchor} Artist:</b> <code>{artist}</code>\n\n<code>{lyrics}</code>"
    try:
        await Pbx.edit(outStr, disable_web_page_preview=True)
    except MessageTooLong:
        content = f"<img src='{image}'/>\n\n{outStr}"
        url = post_to_telegraph(title, content)
        await Pbx.edit(
            f"**{Symbols.anchor} Title:** `{title}`\n**{Symbols.anchor} Artist:** `{artist}`\n\n**{Symbols.anchor} Lyrics:** [Click Here]({url})",
            disable_web_page_preview=True,
        )

HelpMenu("songs").add(
    "song",
    "<song name>",
    "Download the given audio song from Youtube!",
    "song believer",
).add(
    "video",
    "<song name>",
    "Download the given video song from Youtube!",
    "song believer",
).add(
    "lyrics",
    "<song name>",
    "Get the lyrics of the given song! Give artist name after - to get accurate results.",
    "lyrics believer - imagine dragons",
    "Need to setup Lyrics Api key from ",
).info(
    "Song and Lyrics"
).done()
