import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!bella-", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Game(name="jorking my peanits")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("she glup on my shitto til i goober")

bot.run(BOT_TOKEN)