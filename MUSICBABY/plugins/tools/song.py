import os
import future
import asyncio
import yt_dlp
import requests
import wget
import time
import yt_dlp
from urllib.parse import urlparse
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from ... import app
from MUSICBABY import app
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch
from youtubesearchpython import SearchVideos




# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(["song"], ["/", "!", "."]))
async def song(client: Client, message):
    aux = await message.reply_text("**🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...**")
    if len(message.command) < 2:
        return await aux.edit(
            "**🤖 𝐆𝐢𝐯𝐞 🙃 𝐌𝐮𝐬𝐢𝐜 💿 𝐍𝐚𝐦𝐞 😍\n💞 𝐓𝐨 🔊 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 🥀 𝐒𝐨𝐧𝐠❗**"
@app.on_message(filters.command("song"))
def download_song(_, message):
    query = " ".join(message.command[1:])  
    print(query)
    m = message.reply("**🔄 sᴇᴀʀᴄʜɪɴɢ... **")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

        # Add these lines to define views and channel_name
        views = results[0]["views"]
        channel_name = results[0]["channel"]

    except Exception as e:
        m.edit("**⚠️ ɴᴏ ʀᴇsᴜʟᴛs ᴡᴇʀᴇ ғᴏᴜɴᴅ. ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ sᴏɴɢ ɴᴀᴍᴇ**")
        print(str(e))
        return
    m.edit("**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("**📤 ᴜᴘʟᴏᴀᴅɪɴɢ...**")

        message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\nRᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➪{message.from_user.mention}\nVɪᴇᴡs➪ {views}\nCʜᴀɴɴᴇʟ➪ {channel_name}",
            duration=dur
        )
        m.delete()
    except Exception as e:
        m.edit(" - An error !!")
        print(e)

    try:
        song_name = message.text.split(None, 1)[1]
        vid = VideosSearch(song_name, limit=1)
        song_results = vid.result()
        if song_results:
            song_title = song_results["result"][0]["title"]
            song_link = song_results["result"][0]["link"]
        else:
            return await aux.edit("**No results found for the given song name.**")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{song_title}.mp3",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        }
        await aux.edit("**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ...**")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_link])  # Pass song_link as a list
        await aux.edit("**𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ...**")
        audio_path = f"downloads/{song_title}.mp3"
        if os.path.exists(audio_path):
            await message.reply_audio(audio_path)
            os.remove(audio_path)
        else:
            await aux.edit("**Failed to download the audio.**")
        await aux.delete()
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        await aux.edit(f"**Error:** {e}")
        print(e)




# ------------------------------------------------------------------------------- #
