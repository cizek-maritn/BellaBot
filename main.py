import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from gaming import randomize_teams

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!bella-", intents=intents, help_command=None)

@bot.event
async def on_ready():
    activity = discord.Game(name="jorking my peanits")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("she glup on my shitto til i goober")

@bot.command()
async def help(ctx):
    msg="# Hi I'm BellaBot, a Discord bot made by Belladonya!\n"
    msg += "# Here are my commands:\n"
    msg += "## General Commands:\n"
    msg += "!bella-hello - Greet the user, acts as a primitive health check\n"
    msg += "!bella-help - Show this help message\n"
    msg += "## Gaming Commands:\n"
    msg += "!bella-teams <team_count> <player1> <player2> ... - Randomly divides players into teams\n"
    await ctx.send(msg)

@bot.command()
async def teams(ctx, team_count: int, *players):
    if team_count <= 1:
        await ctx.send("Team count must be at least 2.")
        return

    teams = await randomize_teams(" ".join(players), team_count)
    team_messages = [f"**Team {i+1}:** {', '.join(team)}" for i, team in enumerate(teams)]
    await ctx.send("\n".join(team_messages))

bot.run(BOT_TOKEN)