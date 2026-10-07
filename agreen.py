import asyncio
import os
import discord
from discord.ext import commands

# --- CONFIGURATION ---
# ژینگەها Railway یان فایلا .env توکن و ID دبینێت
TOKEN = os.environ.get("DISCORD_TOKEN") or os.environ.get("BOT_TOKEN")
VOICE_CHANNEL_ID = int(
    os.environ.get("VOICE_CHANNEL_ID", "1412910809335726101")
)

# Setup Intents
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def keep_in_vc():
    await bot.wait_until_ready()

    while not bot.is_closed():
        channel = bot.get_channel(VOICE_CHANNEL_ID)

        if channel:
            if not bot.voice_clients:
                try:
                    await channel.connect(reconnect=True, self_deaf=True)
                    print(f"✅ چوە د ناڤ کەناڵێ دەنگی: {channel.name}")
                except Exception as e:
                    print(f"⚠️ ئاریشا گرێدانێ: {e}")
            else:
                vc = bot.voice_clients[0]
                if vc.channel.id != VOICE_CHANNEL_ID:
                    try:
                        await vc.move_to(channel)
                        print(f"🔄 بۆت ڤەگەڕیا بۆ کەناڵێ دیاریکری")
                    except Exception as e:
                        print(f"⚠️ نەشیا کەناڵی بگۆڕێت: {e}")
        else:
            print(
                "❌ ID یێ کەناڵێ دەنگی ناهێتە دۆزین! پشتڕاست بە ژ ژمارەیێ."
            )

        await asyncio.sleep(10)


@bot.event
async def on_ready():
    print(f"🤖 بۆت ب سەرکەوتوویی ئۆنلاین بوو وەک: {bot.user.name}")
    bot.loop.create_task(keep_in_vc())


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        if before.channel is not None and after.channel is None:
            await asyncio.sleep(1)
            channel = bot.get_channel(VOICE_CHANNEL_ID)
            if channel:
                try:
                    await channel.connect(reconnect=True, self_deaf=True)
                    print(f"🔄 بۆت ب ئۆتۆماتیک زڤڕی ب ناڤ VC")
                except Exception as e:
                    print(f"❌ ئاریشا زڤڕینێ: {e}")


if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print(
            "❌ تە تکایە Tokenێ بۆتێ خوە دانیە د ناڤ Railway Variables دا ب ناڤێ DISCORD_TOKEN!"
        )