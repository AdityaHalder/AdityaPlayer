import logging, os, re, sys, time

from os import getenv
from pyrogram import filters
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s:\n%(message)s\n",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)


def logs(name: str) -> logging.Logger:
    return logging.getLogger(name)


_boot_ = time.time()
plugs = {}
chat_admins = {}
chat_links = {}
sudoers = filters.user()


if os.path.exists("Config.env"):
    load_dotenv("Config.env")

try:
    API_ID = int(getenv("API_ID", 0))
    API_HASH = getenv("API_HASH", None)
    BOT_TOKEN = getenv("BOT_TOKEN", None)
    MONGO_URL = getenv("MONGO_URL", None)
    OWNER_ID = int(getenv("OWNER_ID", 0))
    LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
except Exception as e:
    logs(__name__).error(f"❌ Variable Error: {e}")
    sys.exit()


STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

DATABASE_NAME = getenv("DATABASE_NAME", "adityaplayer")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "https://graph.org/file/918101d0ad6b1207e6201.png")





async def sudo_users():
    from .modules.database import adb
    global sudoers
    if OWNER_ID != 0:
        if OWNER_ID not in sudoers:
            sudoers.add(OWNER_ID)
    sudoersdb = adb.sudoers
    sudousers = await sudoersdb.find_one({"sudo": "sudo"})
    sudousers = [] if not sudousers else sudousers["sudoers"]
    if OWNER_ID != 0:
        if OWNER_ID not in sudousers:
            sudousers.append(OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudousers}},
            upsert=True,
        )
    if sudousers:
        for user_id in sudousers:
            if user_id not in sudoers:
                sudoers.add(user_id)
    logs(__name__).info(f"✅ All Sudo Users Loaded.")


