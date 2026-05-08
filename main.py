import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from gaming import random_build, randomize_teams, randomize_gods, latest_god, gacha_links, random_god, get_item_info, hsr_banners

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!bella-", intents=intents, help_command=None, case_insensitive=True)

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
    msg += "Note that commands are case insensitive\n\n"
    msg += "## General Commands:\n"
    msg += "!bella-hello - Greet the user, acts as a primitive health check\n\n"
    msg += "!bella-help - Show this help message\n\n"
    msg += "## Gaming Commands:\n"
    msg += "!bella-teams <team_count> <player1> <player2> ... - Randomly divides players into teams\n\n"
    msg += "!bella-gods <team_count> <aspects> <player1> <player2> ... - Randomly divides players into teams and assigns random Smite 2 gods to each player. Aspects can be true or false\n\n"
    msg += "!bella-latestGod - Shows the latest god added to this bot\n\n"
    msg += "!bella-randomGod - Shows a randomly selected god from Smite 2\n\n"
    msg += "!bella-randomBuild <god> - Shows a random build for the specified god\n\n"
    msg += "!bella-randomGodBuild - Shows a random god and a random build for that god\n\n"
    msg += "!bella-itemInfo <item> - Creates a link to the item's wiki page\n\n"
    msg += "!bella-gacha - Shows a list of useful gacha game links\n\n"
    msg += "!bella-hsrBanners - Shows the current and upcoming Honkai Star Rail banners\n\n"
    await ctx.send(msg)

@bot.command()
async def teams(ctx, team_count: int, *players):
    if team_count <= 1:
        await ctx.send("Team count must be at least 2.")
        return

    teams = await randomize_teams(" ".join(players), team_count)
    team_messages = [f"**Team {i+1}:** {', '.join(team)}" for i, team in enumerate(teams)]
    await ctx.send("\n".join(team_messages))

@bot.command()
async def gods(ctx, team_count: int, aspects: bool, *players):
    if team_count <= 1:
        await ctx.send("Team count must be at least 2.")
        return

    teams = await randomize_teams(" ".join(players), team_count)
    team_gods = await randomize_gods(teams, aspects)
    
    god_messages = []
    for i, (team, gods) in enumerate(zip(teams, team_gods)):
        player_god_pairs = [f"{player} - {god}" for player, god in zip(team, gods)]
        god_messages.append(f"**Team {i+1}:** {', '.join(player_god_pairs)}")
    
    await ctx.send("\n".join(god_messages))

@bot.command()
async def latestGod(ctx):
    god = await latest_god()
    await ctx.send(f"bella-gods latest god: **{god}**")

@bot.command()
async def randomGod(ctx):
    god = await random_god()
    await ctx.send(f"Your random god is: **{god}**")

@bot.command()
async def randomBuild(ctx, god: str):
    build_msg = await random_build(god)
    await ctx.send(build_msg)

@bot.command()
async def randomGodBuild(ctx):
    god = await random_god()
    build_msg = await random_build(god)
    await ctx.send(build_msg)

@bot.command()
async def itemInfo(ctx, *, item: str):
    info = await get_item_info(item)
    await ctx.send(info)

@bot.command()
async def gacha(ctx):
    links = await gacha_links()
    await ctx.send(links)

@bot.command()
async def hsrBanners(ctx):
    banners = await hsr_banners()
    await ctx.send(banners)

bot.run(BOT_TOKEN)