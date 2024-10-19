import os

import discord
from dotenv import load_dotenv

from commands import showcase
from views.showcase import FullShowcaseView

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
        return
    characters = showcase.get_character_showcase(uid)
    embed_field = "```\n"
    for character in characters:
        embed_field += "%-15s \n" % (
            character
        )
    embed_field += "```"
    embed = discord.Embed(
        title="Character Showcase"
    )
    embed.add_field(name="Characters", value=embed_field)
    await ctx.respond(
        embed=embed,
        view=FullShowcaseView(characters)
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


bot.run(os.environ["BOT_TOKEN"])
