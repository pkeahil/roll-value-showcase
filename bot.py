import json
import os

import discord
import pandas as pd
from dotenv import load_dotenv

import builds
import db
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
async def showcase_rv(ctx: discord.ApplicationContext, uid: str = None):
    if not uid:
        await ctx.respond("No uid provided")
        return

    characters = showcase.get_character_showcase(uid)
    current_showcase = pd.DataFrame.from_dict(characters, orient="index")
    current_showcase["character_name"] = current_showcase.index

    saved_showcase = db.get_saved_builds(db.showcase_db_connection(), uid)

    curr = set(current_showcase["id"].to_list())
    saved_showcase = saved_showcase[~saved_showcase["id"].isin(curr)]
    showcase_total = pd.concat([current_showcase, saved_showcase])
    builds.save(db.showcase_db_connection(), showcase_total, uid)

    characters = json.loads(showcase_total.to_json(orient="index"))
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
        view=FullShowcaseView(characters, ctx.author.id)
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


bot.run(os.environ["BOT_TOKEN"])
