import os

import discord
from dotenv import load_dotenv

from commands import showcase

load_dotenv()
bot = discord.Bot()


@bot.slash_command()
async def hello_world(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!")


@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.slash_command()
async def showcase_rv(ctx, uid: str = None):
    if not uid:
        await ctx.respond("No uid provided")
    showcase_result = showcase.get_character_showcase(uid)
    await ctx.respond(showcase_result)

bot.run(os.environ["BOT_TOKEN"])
