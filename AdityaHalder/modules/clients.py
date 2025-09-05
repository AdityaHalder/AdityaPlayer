import sys

from .. import console
from .database import get_assistant, group_assistant
from .helpers import AssistantErr

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls import PyTgCalls, filters as fl
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import Call, GroupCallConfig, ChatUpdate, Update, StreamEnded


assistants = []
assistantids = []




class Bot(Client):
    def __init__(self):
        super().__init__(
            "Aditya_Server",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            bot_token=console.BOT_TOKEN,
        )

    async def start(self):
        console.logs(__name__).info(f"🤖 Starting Bot ...")
        await super().start()
        get_me = await self.get_me()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        self.username = get_me.username
        self.mention = get_me.mention
        self.id = get_me.id
        try:
            await self.send_message(
                console.LOG_GROUP_ID, "**🤖 Bot Started.**"
            )
        except:
            console.logs(__name__).error(
                "❌ Bot has failed to access the log Group. Make sure that you have added your bot to your log group and promoted as admin!"
            )
            sys.exit()
        try:
            a = await self.get_chat_member(console.LOG_GROUP_ID, self.id)
        except:
            console.logs(__name__).error(
                "❌ Bot has failed to access the log Group. Make sure that you have added your bot to your log group and promoted as admin!"
            )
            sys.exit()
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            console.logs(__name__).error(
                "⚠️ Please promote bot as admin in your logger group!"
            )
            sys.exit()
        console.logs(__name__).info(f"🤖 Bot Started as {self.name}")
    
    
    
    
class App(Client):
    def __init__(self):
        self.one = Client(
            "Aditya_Halder_1",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING1),
            no_updates=True,
        )
        self.two = Client(
            "Aditya_Halder_2",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING2),
            no_updates=True,
        )
        self.three = Client(
            "Aditya_Halder_3",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING3),
            no_updates=True,
        )
        self.four = Client(
            "Aditya_Halder_4",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING4),
            no_updates=True,
        )
        self.five = Client(
            "Aditya_Halder_5",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING5),
            no_updates=True,
        )
    
    
    async def start(self):
        console.logs(__name__).info(f"🦋 Starting Assistant Clients")
        if console.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("AdityaServer")
                await self.one.join_chat("AdityaDiscus")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(
                    console.LOG_GROUP_ID, "**🦋 Assistant (1) Started.**"
                )
            except:
                console.logs(__name__).error(
                    f"❌ Assistant account 1 has failed to access the log group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            get_me = await self.one.get_me()
            if get_me.last_name:
                self.one.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.one.name = get_me.first_name
            self.one.username = get_me.username
            self.one.mention = get_me.mention
            self.one.id = get_me.id
            assistantids.append(get_me.id)
            console.logs(__name__).info(
                f"🦋 Assistant (1) started as - {self.one.name}"
            )
        if console.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("AdityaServer")
                await self.two.join_chat("AdityaDiscus")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(
                    console.LOG_GROUP_ID, "**🦋 Assistant (2) Started.**"
                )
            except:
                console.logs(__name__).error(
                    f"❌ Assistant account 2 has failed to access the log group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            get_me = await self.two.get_me()
            if get_me.last_name:
                self.two.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.two.name = get_me.first_name
            self.two.username = get_me.username
            self.two.mention = get_me.mention
            self.two.id = get_me.id
            assistantids.append(get_me.id)
            console.logs(__name__).info(
                f"🦋 Assistant (2) started as - {self.two.name}"
            )
        if console.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("AdityaServer")
                await self.three.join_chat("AdityaDiscus")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(
                    console.LOG_GROUP_ID, "**🦋 Assistant (3) Started.**"
                )
            except:
                console.logs(__name__).error(
                    f"❌ Assistant account 3 has failed to access the log group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            get_me = await self.three.get_me()
            if get_me.last_name:
                self.three.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.three.name = get_me.first_name
            self.three.username = get_me.username
            self.three.mention = get_me.mention
            self.three.id = get_me.id
            assistantids.append(get_me.id)
            console.logs(__name__).info(
                f"🦋 Assistant (3) started as - {self.three.name}"
            )
        if console.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("AdityaServer")
                await self.four.join_chat("AdityaDiscus")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(
                    console.LOG_GROUP_ID, "**🦋 Assistant (4) Started.**"
                )
            except:
                console.logs(__name__).error(
                    f"❌ Assistant (4) account has failed to access the log group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            get_me = await self.four.get_me()
            if get_me.last_name:
                self.four.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.four.name = get_me.first_name
            self.four.username = get_me.username
            self.four.mention = get_me.mention
            self.four.id = get_me.id
            assistantids.append(get_me.id)
            console.logs(__name__).info(
                f"🦋 Assistant (4) started as - {self.four.name}"
            )
        if console.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("AdityaServer")
                await self.five.join_chat("AdityaDiscus")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(
                    console.LOG_GROUP_ID, "**🦋 Assistant (5) Started.**"
                )
            except:
                console.logs(__name__).error(
                    f"Assistant (5) account has failed to access the log group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                sys.exit()
            get_me = await self.five.get_me()
            if get_me.last_name:
                self.five.name = (
                    get_me.first_name + " " + get_me.last_name
                )
            else:
                self.five.name = get_me.first_name
            self.five.username = get_me.username
            self.five.mention = get_me.mention
            self.five.id = get_me.id
            assistantids.append(get_me.id)
            console.logs(__name__).info(
                f"🦋 Assistant (5) started as - {self.five.name}"
            )




class Call(PyTgCalls):
    def __init__(self):
        self.adityaplayer1 = Client(
            "Aditya_Player_1",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING1),
        )
        self.one = PyTgCalls(
            self.adityaplayer1, cache_duration=100
        )
        self.adityaplayer2 = Client(
            "Aditya_Player_2",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING2),
        )
        self.two = PyTgCalls(
            self.adityaplayer2, cache_duration=100
        )
        self.adityaplayer3 = Client(
            "Aditya_Player_3",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING3),
        )
        self.three = PyTgCalls(
            self.adityaplayer3, cache_duration=100
        )
        self.adityaplayer4 = Client(
            "Aditya_Player_4",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING4),
        )
        self.four = PyTgCalls(
            self.adityaplayer4, cache_duration=100
        )
        self.adityaplayer5 = Client(
            "Aditya_Player_5",
            api_id=console.API_ID,
            api_hash=console.API_HASH,
            session_string=str(console.STRING5),
        )
        self.five = PyTgCalls(
            self.adityaplayer5, cache_duration=100
        )
        
    call_config = GroupCallConfig(auto_start=False)

    
    paused = {}
    queue = {}

    
    active_chats = []



    async def ensure_assistant_in_chat(self, chat_id):
        from .. import bot
        assistant = await get_assistant(chat_id)
        
        async def try_join():
            chat = await bot.get_chat(chat_id)
            try:
                if chat.username:
                    link_or_username = chat.username
                    chat_link = f"https://t.me/{link_or_username}"
                else:
                    try:
                        link_or_username = await bot.export_chat_invite_link(chat_id)
                        chat_link = link_or_username
                    except errors.ChatAdminRequired:
                        raise AssistantErr("❌ Bot needs admin rights with **Invite Users via Link** permission.")

                await assistant.join_chat(link_or_username)
                console.chat_links[chat_id] = chat_link
                return True
            
            except errors.ChatWriteForbidden:
            
                try:
                    await bot.approve_chat_join_request(chat_id, assistant.id)
                    return True
                except errors.ChatAdminRequired:
                    raise AssistantErr("⚠️ Assistant requested to join, but bot has no rights to approve.")
                except Exception:
                    raise AssistantErr("⚠️ Assistant requested to join. Please approve manually.")
            

            except errors.InviteHashExpired:
                raise AssistantErr("❌ The invite link expired.")
            except errors.InviteHashInvalid:
                raise AssistantErr("❌ The invite link is invalid.")
            except errors.UserAlreadyParticipant:
                raise AssistantErr("ℹ️ Assistant already participant.")
            except errors.FloodWait as e:
                raise AssistantErr(f"⏳ FloodWait: must wait `{e.value}` seconds.")
            except errors.ChatAdminRequired:
                raise AssistantErr("❌ Bot needs admin rights in this chat.")
            except errors.UserRestricted:
                raise AssistantErr("❌ Assistant is restricted and cannot join chats.")
            except errors.UserBannedInChannel:
                raise AssistantErr("❌ Assistant is banned from this chat.")
            except errors.ChannelPrivate:
                raise AssistantErr("❌ Chat is private or link revoked.")
            except Exception as e:
                raise AssistantErr(f"⚠️ Unexpected error while assistant tried to join:\n`{e}`")
        

        try:
            member = await bot.get_chat_member(chat_id, assistant.id)

            if member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                return True

            elif member.status == ChatMemberStatus.BANNED:
                try:
                    await bot.unban_chat_member(chat_id, assistant.id)
                    return await try_join()
                except Exception:
                    raise AssistantErr("🚫 Assistant is banned in this chat. Please unban first.")

            elif member.status == ChatMemberStatus.LEFT:
                return await try_join()

            else:
                raise AssistantErr(f"⚠️ Assistant is in the chat but with status `{member.status}`.")
            
        except errors.UserNotParticipant:
            return await try_join()

        except errors.ChatAdminRequired:
            raise AssistantErr("❌ Bot has no rights to check chat members.")

        except Exception as e:
            raise AssistantErr(f"⚠️ Unexpected error while checking:\n`{e}`")
        

    
    

    async def change_stream(self, chat_id: int):
        from .. import bot
        await self.pop_queue(chat_id)
    
        queued = self.queue.get(chat_id)
        if not queued:
            await bot.send_message(chat_id, "**❎ Queue is empty, So left\nfrom VC❗...**")
            return await self.close_stream(chat_id)

        aux = await bot.send_message(chat_id, "**🔁 Processing ✨...**")
        pos  = 0
        media_stream = queued[0].get("media_stream")

        await self.start_stream(chat_id, media_stream)
    
        thumbnail = queued[0].get("thumbnail")
        title = queued[0].get("title")
        duration = queued[0].get("duration")
        mention = queued[0].get("requested_by")
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🗑️ Close", callback_data="close"
                    )
                ],
            ]
        )
        caption = f"""
✅ **Started Streaming On VC.**

**❍ Title:** [{title}...](https://t.me/{bot.me.username})
**❍ Duration:** {duration}
**❍ Requested By:** {mention}"""
        try:
            await aux.delete()
        except Exception:
            pass
        await bot.send_photo(chat_id, photo=thumbnail, caption=caption, has_spoiler=True, reply_markup=buttons)
    



    
    async def start_stream(self, chat_id: int, media_stream):
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.play(chat_id, media_stream, config=self.call_config)
            if chat_id not in self.active_chats:
                self.active_chats.append(chat_id)
        except NoActiveGroupCall:
            await self.ensure_assistant_in_chat(chat_id)
            await assistant.play(chat_id, media_stream, config=self.call_config)
            if chat_id not in self.active_chats:
                self.active_chats.append(chat_id)
        
    
    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume(chat_id)

    async def mute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.mute(chat_id)

    async def unmute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.unmute(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.leave_call(chat_id)
        
        




    async def add_to_queue(
        self, chat_id, media_stream, title, duration, thumbnail, requested_by
    ):
        if chat_id not in self.queue:
            self.queue[chat_id] = []
    
        item = {
            "media_stream": media_stream,
            "title": title,
            "duration": duration,
            "thumbnail": thumbnail,
            "requested_by": requested_by
        }
        self.queue[chat_id].append(item)
    
        return len(self.queue[chat_id]) - 1


    async def pop_queue(self, chat_id: int):
        if chat_id in self.queue and self.queue[chat_id]:
            return self.queue[chat_id].pop(0)
        return None


    async def clear_queue(self, chat_id: int):
        if chat_id in self.active_chats:
            self.active_chats.remove(chat_id)
            
        try:
            self.queue.pop(chat_id)
        except:
            pass



    async def is_stream_off(self, chat_id: int) -> bool:
        mode = self.paused.get(chat_id)
        if not mode:
            return False
        return mode


    async def stream_on(self, chat_id: int):
        self.paused[chat_id] = False


    async def stream_off(self, chat_id: int):
        self.paused[chat_id] = True


    async def close_stream(self, chat_id: int):
        try:
            await self.stop_stream(chat_id)
        except Exception:
            pass
        await self.clear_queue(chat_id)



    
        
        
    async def ping(self):
        pings = []
        if console.STRING1:
            pings.append(await self.one.ping)
        if console.STRING2:
            pings.append(await self.two.ping)
        if console.STRING3:
            pings.append(await self.three.ping)
        if console.STRING4:
            pings.append(await self.four.ping)
        if console.STRING5:
            pings.append(await self.five.ping)
        
        return str(round(sum(pings) / len(pings), 3))


    async def start(self):
        console.logs(__name__).info("🎧 Starting PyTgCalls Client\n")
        if console.STRING1:
            await self.one.start()
        if console.STRING2:
            await self.two.start()
        if console.STRING3:
            await self.three.start()
        if console.STRING4:
            await self.four.start()
        if console.STRING5:
            await self.five.start()
        



    async def decorators(self):
        @self.one.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
        @self.two.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
        @self.three.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
        @self.four.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
        @self.five.on_update(fl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
        @self.one.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
        @self.two.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
        @self.three.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
        @self.four.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
        @self.five.on_update(fl.chat_update(ChatUpdate.Status.KICKED))
        @self.one.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
        @self.two.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
        @self.three.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
        @self.four.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
        @self.five.on_update(fl.chat_update(ChatUpdate.Status.LEFT_GROUP))
        async def stream_services_handler(_, update: Update):
            return await self.close_stream(update.chat_id)
    

        @self.one.on_update(fl.stream_end())
        @self.two.on_update(fl.stream_end())
        @self.three.on_update(fl.stream_end())
        @self.four.on_update(fl.stream_end())
        @self.five.on_update(fl.stream_end())
        async def stream_end_handler(_, update: Update):
            chat_id = update.chat_id
            return await self.change_stream(chat_id)




