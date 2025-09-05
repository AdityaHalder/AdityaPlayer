import aiofiles, aiohttp, base64, json, os, random, re, requests

from .. import app, bot, call, cdz, console
from urllib.parse import urlparse
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ntgcalls import TelegramServerError
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import MediaStream
from pytgcalls.types import AudioQuality, VideoQuality
from youtubesearchpython.__future__ import VideosSearch



def parse_query(query: str) -> str:
    if bool(re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|shorts/|live/)?([A-Za-z0-9_-]{11})(?:[?&].*)?$', query)):
        match = re.search(r'(?:v=|\/(?:embed|v|shorts|live)\/|youtu\.be\/)([A-Za-z0-9_-]{11})', query)
        if match:
            return f"https://www.youtube.com/watch?v={match.group(1)}"
        
    return query



def parse_tg_link(link: str):
    parsed = urlparse(link)
    path = parsed.path.strip('/')
    parts = path.split('/')
    
    if len(parts) >= 2:
        return str(parts[0]), int(parts[1])
        
    return None, None


async def fetch_song(query: str):
    url = "http://82.180.147.88:1470/song"
    params = {"query": query}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                try:
                    return await response.json()
                except Exception:
                    return {}
                
            return {}

def convert_to_seconds(duration: str) -> int:
    parts = list(map(int, duration.split(":")))
    total = 0
    multiplier = 1

    for value in reversed(parts):
        total += value * multiplier
        multiplier *= 60

    return total


def format_duration(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if sec > 0 or not parts:
        parts.append(f"{sec}s")

    return " ".join(parts)



def seconds_to_hhmmss(seconds):
    if seconds < 3600:
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02}:{sec:02}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        sec = seconds % 60
        return f"{hours:d}:{minutes:02}:{sec:02}"


def random_color():
    return (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))


def trim_text(draw, text, font, max_width):
    """Ensure text fits inside max_width, otherwise trim and add '...'"""
    if not text:
        return ""
    original = text
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            break
        text = text[:-1]
    if text != original:
        while True:
            bbox = draw.textbbox((0, 0), text + "...", font=font)
            if bbox[2] - bbox[0] <= max_width or len(text) == 0:
                break
            text = text[:-1]
        text = text + "..."
    return text
    

async def create_music_thumbnail(cover_path, title, artist, duration_seconds=None, output_path="thumbnail.png"):
    # Handle title/artist
    if not title or title.strip() == "":
        title = "Unknown Title"
    if not artist or artist.strip() == "":
        artist = "Unknown Artist"

    # Handle time
    if (
        duration_seconds is None
        or duration_seconds == 0
        or duration_seconds == "live"
    ):
        total_time = "Live"
        tot_sec = None
    else:
        tot_sec = duration_seconds
        total_time = seconds_to_hhmmss(duration_seconds)

    if tot_sec:
        cur_sec = random.randint(0, tot_sec)
        current_time = seconds_to_hhmmss(cur_sec)
    else:
        cur_sec = random.randint(0, 7200)
        current_time = seconds_to_hhmmss(cur_sec)

    # Load cover and background
    cover = Image.open(cover_path).convert("RGBA").resize((500, 500))
    bg = cover.copy().resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(25))

    # --- Gradient overlay background ---
    grad_overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad_overlay)
    c1, c2 = random_color(), random_color()
    for i in range(bg.height):
        r = int(c1[0] + (c2[0]-c1[0]) * (i/bg.height))
        g = int(c1[1] + (c2[1]-c1[1]) * (i/bg.height))
        b = int(c1[2] + (c2[2]-c1[2]) * (i/bg.height))
        gdraw.line([(0, i), (bg.width, i)], fill=(r, g, b, 80))
    bg = Image.alpha_composite(bg, grad_overlay)

    # --- Glassmorphic Player Card ---
    card_w, card_h = 700, 380
    border_thickness = 5  

    # gradient for card border
    grad = Image.new("RGBA", (card_w + border_thickness*2, card_h + border_thickness*2), (0,0,0,0))
    gdraw = ImageDraw.Draw(grad)
    c1, c2 = random_color(), random_color()
    for i in range(grad.height):
        r = int(c1[0] + (c2[0]-c1[0]) * (i/grad.height))
        g = int(c1[1] + (c2[1]-c1[1]) * (i/grad.height))
        b = int(c1[2] + (c2[2]-c1[2]) * (i/grad.height))
        gdraw.line([(0, i), (grad.width, i)], fill=(r, g, b))

    mask_outer = Image.new("L", grad.size, 0)
    mask_inner = Image.new("L", (card_w, card_h), 0)
    d_outer = ImageDraw.Draw(mask_outer)
    d_inner = ImageDraw.Draw(mask_inner)

    d_outer.rounded_rectangle([0, 0, grad.width, grad.height], 36, fill=255)
    d_inner.rounded_rectangle([0, 0, card_w, card_h], 30, fill=255)

    mask_inner_padded = Image.new("L", grad.size, 0)
    mask_inner_padded.paste(mask_inner, (border_thickness, border_thickness))
    mask_outer.paste(0, (0,0), mask_inner_padded)

    border = Image.composite(grad, Image.new("RGBA", grad.size, (0,0,0,0)), mask_outer)

    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 60))
    mask_card = Image.new("L", (card_w, card_h), 0)
    ImageDraw.Draw(mask_card).rounded_rectangle([0,0,card_w,card_h], 30, fill=255)

    card_with_border = border.copy()
    card_with_border.paste(card, (border_thickness, border_thickness), mask_card)

    # position card CENTER
    x = (bg.width - card_with_border.width) // 2
    y = (bg.height - card_with_border.height) // 2
    bg.paste(card_with_border, (x,y), card_with_border)

    # --- Album cover inside card with gradient border ---
    cover_size = 200
    border_size = 6  # thin border

    # Gradient border for cover
    grad_cover = Image.new("RGBA", (cover_size + border_size*2, cover_size + border_size*2), (0,0,0,0))
    gdraw = ImageDraw.Draw(grad_cover)
    c1, c2 = random_color(), random_color()
    for i in range(grad_cover.height):
        r = int(c1[0] + (c2[0]-c1[0]) * (i/grad_cover.height))
        g = int(c1[1] + (c2[1]-c1[1]) * (i/grad_cover.height))
        b = int(c1[2] + (c2[2]-c1[2]) * (i/grad_cover.height))
        gdraw.line([(0, i), (grad_cover.width, i)], fill=(r, g, b))

    mask_outer = Image.new("L", grad_cover.size, 0)
    mask_inner = Image.new("L", (cover_size, cover_size), 0)
    d_outer = ImageDraw.Draw(mask_outer)
    d_inner = ImageDraw.Draw(mask_inner)

    d_outer.rounded_rectangle([0,0,grad_cover.width,grad_cover.height], 30, fill=255)
    d_inner.rounded_rectangle([0,0,cover_size,cover_size], 26, fill=255)

    mask_inner_padded = Image.new("L", grad_cover.size, 0)
    mask_inner_padded.paste(mask_inner, (border_size, border_size))
    mask_outer.paste(0, (0,0), mask_inner_padded)

    border_cover = Image.composite(grad_cover, Image.new("RGBA", grad_cover.size, (0,0,0,0)), mask_outer)

    cover_resized = cover.resize((cover_size, cover_size))
    mask_cover = Image.new("L", (cover_size, cover_size), 0)
    ImageDraw.Draw(mask_cover).rounded_rectangle([0,0,cover_size,cover_size], 26, fill=255)

    cover_with_border = border_cover.copy()
    cover_with_border.paste(cover_resized, (border_size, border_size), mask_cover)

    cover_x = x + border_thickness + 30
    cover_y = y + (card_h - cover_with_border.height)//2 + border_thickness
    bg.paste(cover_with_border, (cover_x, cover_y), cover_with_border)

    # --- Draw texts and progress bar ---
    draw = ImageDraw.Draw(bg)
    font_title = ImageFont.truetype("AdityaHalder/resource/font.ttf", 36)
    font_artist = ImageFont.truetype("AdityaHalder/resource/font.ttf", 28)
    font_time = ImageFont.truetype("AdityaHalder/resource/font.ttf", 24)

    max_width = card_w - 300
    title = trim_text(draw, title, font_title, max_width)
    artist = trim_text(draw, artist, font_artist, max_width)

    text_x = cover_x + cover_with_border.width + 30
    draw.text((text_x, y + 86), title, font=font_title, fill="white")
    draw.text((text_x, y + 146), artist, font=font_artist, fill="white")

    # Progress bar
    progress_x, progress_y = text_x, y + 206
    bar_w, bar_h = 380, 8
    prog_fill = int((cur_sec / tot_sec) * bar_w) if tot_sec else bar_w

    draw.rounded_rectangle([progress_x, progress_y, progress_x + bar_w, progress_y + bar_h],
                           5, fill=(120, 120, 120, 160))

    c1, c2 = random_color(), random_color()
    for i in range(prog_fill):
        r = int(c1[0] + (c2[0]-c1[0]) * (i/max(1, prog_fill)))
        g = int(c1[1] + (c2[1]-c1[1]) * (i/max(1, prog_fill)))
        b = int(c1[2] + (c2[2]-c1[2]) * (i/max(1, prog_fill)))
        draw.line([(progress_x + i, progress_y), (progress_x + i, progress_y + bar_h)], fill=(r,g,b))

    knob_x = progress_x + prog_fill
    knob_y = progress_y + bar_h // 2
    draw.ellipse([knob_x - 6, knob_y - 6, knob_x + 6, knob_y + 6], fill="white", outline="black", width=2)

    draw.text((progress_x, progress_y + 15), current_time, font=font_time, fill="white")
    total_bbox = draw.textbbox((0, 0), total_time, font=font_time)
    total_x = progress_x + bar_w - (total_bbox[2] - total_bbox[0])
    draw.text((total_x, progress_y + 15), total_time, font=font_time, fill="red" if total_time == "Live" else "white")

    # Controls (with repeat moved before back)
    controls_y = progress_y + 70
    num_icons = 7
    step = bar_w // (num_icons - 1)
    icon_positions = [progress_x + i*step for i in range(num_icons)]

    # shuffle
    shuffle_x = icon_positions[0]
    draw.line([(shuffle_x-12, controls_y-8), (shuffle_x+8, controls_y+12)], fill=(0,255,120), width=3)
    draw.polygon([(shuffle_x+8, controls_y+12), (shuffle_x+16, controls_y+6), (shuffle_x+2, controls_y+4)], fill=(0,255,120))
    draw.line([(shuffle_x-12, controls_y+8), (shuffle_x-2, controls_y-2)], fill=(0,255,120), width=3)

    # repeat (bright yellow)
    repeat_x = icon_positions[1]
    repeat_color = (255, 220, 50)
    draw.arc([repeat_x-14, controls_y-12, repeat_x+14, controls_y+12], start=30, end=300, fill=repeat_color, width=3)
    draw.polygon([(repeat_x+14, controls_y-2), (repeat_x+22, controls_y-6), (repeat_x+14, controls_y-10)], fill=repeat_color)

    # back
    sbx = icon_positions[2]
    draw.polygon([(sbx+10, controls_y-10), (sbx+10, controls_y+10), (sbx-12, controls_y)], fill="white")
    draw.rectangle([sbx+14, controls_y-10, sbx+18, controls_y+10], fill="white")

    # pause
    center_x = icon_positions[3]
    bar_wid, bar_height = 6, 26
    gap = 10
    draw.rectangle([center_x-gap-bar_wid, controls_y-bar_height//2, center_x-gap, controls_y+bar_height//2], fill="white")
    draw.rectangle([center_x+gap, controls_y-bar_height//2, center_x+gap+bar_wid, controls_y+bar_height//2], fill="white")

    # forward
    sfx = icon_positions[4]
    draw.polygon([(sfx-10, controls_y-10), (sfx-10, controls_y+10), (sfx+12, controls_y)], fill="white")
    draw.rectangle([sfx-18, controls_y-10, sfx-14, controls_y+10], fill="white")

    # heart
    fav_x = icon_positions[5]
    heart = [(fav_x, controls_y), (fav_x-10, controls_y-10), (fav_x-20, controls_y), (fav_x, controls_y+14),
             (fav_x+20, controls_y), (fav_x+10, controls_y-10)]
    draw.polygon(heart, fill="red")

    # earphone
    ear_x = icon_positions[6]
    draw.arc([ear_x-20, controls_y-20, ear_x+20, controls_y+20], start=200, end=-20, fill="white", width=3)
    draw.rectangle([ear_x-18, controls_y-4, ear_x-10, controls_y+12], fill="white")
    draw.rectangle([ear_x+10, controls_y-4, ear_x+18, controls_y+12], fill="white")

    bg.save(output_path)
    return output_path


async def generate_thumbnail(url: str) -> str:
    try:
        filename = os.path.join("cache", f"thumbnail_{hash(url)}.jpg")
        parsed = urlparse(url)

        if parsed.scheme in ("http", "https"):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return ""
                    data = await resp.read()

                    with Image.open(BytesIO(data)) as img:
                        img = img.resize((1280, 720))
                        buf = BytesIO()
                        img.save(buf, format="JPEG", quality=90)
                        buf.seek(0)

                        async with aiofiles.open(filename, "wb") as f:
                            await f.write(buf.read())

        else:
            if not os.path.isfile(url):
                return "AdityaHalder/rsource/thumbnail.png"

            with Image.open(url) as img:
                img = img.resize((1280, 720))
                buf = BytesIO()
                img.save(buf, format="JPEG", quality=90)
                buf.seek(0)

                async with aiofiles.open(filename, "wb") as f:
                    await f.write(buf.read())

        return filename

    except Exception:
        return "AdityaHalder/rsource/thumbnail.png"


async def make_thumbnail(image, title, channel, duration, output):
    return await create_music_thumbnail(image, title, channel, duration, output)




@bot.on_message(cdz(["play", "vplay"]) & ~filters.private)
async def start_stream_in_vc(client, message):
    try:
        await message.delete()
    except Exception:
        pass
    chat_id = message.chat.id
    mention = (
        message.from_user.mention
        if message.from_user else
        f"[Anonymous User](https://t.me/{bot.username})"
    )
    replied = message.reply_to_message
    audio_telegram = replied.audio or replied.voice if replied else None
    video_telegram = replied.video or replied.document if replied else None
    
    if audio_telegram or video_telegram:
        if audio_telegram:
            id = audio_telegram.file_unique_id
            try:
                file_name = (
                    audio_telegram.file_unique_id
                    + "."
                    + (
                        (audio_telegram.file_name.split(".")[-1])
                        if (not isinstance(audio_telegram, Voice))
                        else "ogg"
                    )
                )
            except:
                file_name = audio_telegram.file_unique_id + "." + "ogg"
            file_name = os.path.join(
                os.path.realpath("downloads"), file_name
            )
            duration_sec = audio_telegram.duration
            
        if video_telegram:
            id = video_telegram.file_unique_id
            try:
                file_name = (
                    video_telegram.file_unique_id
                    + "."
                    + (video_telegram.file_name.split(".")[-1])
                )
            except:
                file_name = video_telegram.file_unique_id + "." + "mp4"
            file_name = os.path.join(
                os.path.realpath("downloads"), file_name
            )
            duration_sec = video_telegram.duration
            
        duration_mins = format_duration(duration_sec)
        views = "None"
        image_path = "AdityaHalder/resource/thumbnail.png"
        channellink = (
            f"https://t.me/{message.chat.username}"
            if message.chat.username
            else "Telegram Channel"
        )
        channel = message.chat.title
        link = message.link
        
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                f"""
**🥀 Give Me Some Query To
Stream Audio Or Video❗...

ℹ️ Example:
≽ Audio: `/play yalgaar`
≽ Video: `/vplay yalgaar`**"""
            )
        query = parse_query(" ".join(message.command[1:]))
        try:
            aux =  await message.reply_text("**🔄 Processing ✨...**")
        except Exception:
            pass
        video_stream = True if message.command[0].startswith("v") else False

        search = VideosSearch(query, limit=1)
        result = (await search.next())["result"]

        if not result:
            try:
                return await aux.edit("❌ No results found.")
            except Exception:
                return

        video = result[0]
        full_title = video["title"]
        title = full_title[:30]
        id = video["id"]
        duration = video["duration"]
        if not duration:
            try:
                return await aux.edit("❌ I can't stream live-stream right now.")
            except Exception:
                return
        duration_sec = convert_to_seconds(duration)
        duration_mins = format_duration(duration_sec)
        views = video["viewCount"]["short"]
        image_path = video["thumbnails"][0]["url"].split("?")[0]
        channellink = video["channel"]["link"]
        channel = video["channel"]["name"]
        link = video["link"]
        xyz = os.path.join("downloads", f"{id}.mp3")
        if not os.path.exists(xyz):
            song_data = await fetch_song(query)
            if not song_data:
                try:
                    return await aux.edit("❌ Failed to process query, please try again.")
                except Exception:
                    return
            song_url = song_data["link"]
            
            c_username, message_id = parse_tg_link(song_url)
            msg = await client.get_messages(c_username, message_id)
            try:
                try:
                    await aux.edit("**⬇️ Downloading ✨...**")
                except Exception:
                    pass
                await msg.download(file_name=xyz)
            except Exception:
                try:
                    return await aux.edit("❌ Failed to download, please try again.")
                except Exception:
                    return
                    
            while not os.path.exists(xyz):
                await asyncio.sleep(0.5)
                
        file_path = xyz

    
    media_stream = (
        MediaStream(
            media_path=file_path,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
        )
        if not video_stream
        else MediaStream(
            media_path=file_path,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
        )
    )
    
    if chat_id not in call.queue:
        try:
            try:
                await call.start_stream(chat_id, media_stream)
            except NoActiveGroupCall:
                try:
                    return await aux.edit("❌ No active vc found to stream.")
                except Exception:
                    return
            except TelegramServerError:
                try:
                    return await aux.edit(
                        "⚠️**Telegram server error!**\nPlease try again shortly."
                    )
                except Exception:
                    return
        except Exception as e:
            try:
                return await aux.edit(
                    f"❌ **Failed to stream**❗\n\n`{e}`"
                )
            except Exception:
                return

    image_file = await generate_thumbnail(image_path)
    thumbnail = await make_thumbnail(
        image_file, full_title, channel, duration_sec, f"cache/{chat_id}_{id}_{message.id}.png"
    )
        
    try:
        await aux.delete()
    except:
        pass
        
    pos = await call.add_to_queue(chat_id, media_stream, title, duration_mins, thumbnail, mention)
    status = (
        "✅ **Started Streaming in VC.**"
        if pos == 0
        else f"✅ **Added To Queue At: #{pos}**"
    )
    caption = f"""
{status}

**❍ Title:** [{title}...]({link})
**❍ Duration:** {duration_mins}
**❍ Requested By:** {mention}"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🗑️ Close",
                    callback_data="close",
                ),
            ]
        ]
    )
    try:
        await message.reply_photo(photo=thumbnail, caption=caption, has_spoiler=True, reply_markup=buttons)
    except Exception as e:
        pass

    if chat_id != console.LOG_GROUP_ID:
        try:
            chat_name = message.chat.title
            if message.chat.username:
                chat_link = f"@{message.chat.username}"
            elif chat_id in console.chat_links:
                clink = console.chat_links[chat_id]
                chat_link = f"[Private Chat]({clink})"
            else:
                try:
                    new_link = await client.export_chat_invite_link(chat_id)
                    console.chat_links[chat_id] = new_link
                    chat_link = f"[Private Chat]({new_link})"
                except Exception:
                    chat_link = "N/A"
        

            if message.from_user:
                if message.from_user.username:
                    req_user = f"@{message.from_user.username}"
                else:
                    req_user = message.from_user.mention
                user_id = message.from_user.id
            elif message.sender_chat:
                if message.sender_chat.username:
                    req_user = f"@{message.sender_chat.username}"
                else:
                    req_user = message.sender_chat.title
                user_id = message.sender_chat.id
            else:
                req_user = "Anonymous User"
                user_id = "N/A"

            stream_type = "Audio" if not video_stream else "Video"

            log_message = f"""
🎉 **{mention} Just Played A Song.**

📍 **Chat:** {chat_name}
💬 **Chat Link:** {chat_link}
♂️ **Chat ID:** {chat_id}
👤 **Requested By:** {req_user}
🆔 **User ID:** `{user_id}`
🔎 **Query:** {query}
🎶 **Title:** [{title}...]({link})
⏱️ **Duration:** {duration_mins}
📡 **Stream Type:** {stream_type}"""
            await bot.send_photo(console.LOG_GROUP_ID, photo=thumbnail, caption=log_message)
        except Exception:
            pass















