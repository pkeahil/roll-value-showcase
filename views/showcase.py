
import discord


class SelectCharacters(discord.ui.Select):
    def __init__(self, characters=None, active_character: str = None):
        self.characters = characters
        options = []
        for character in characters:
            options.append(discord.SelectOption(label=character))
        super().__init__(
            options=options,
            placeholder=active_character if active_character else "Select..."
        )

    async def callback(
            self,
            interaction: discord.Interaction):
        character_name = self.values[0]
        embed_field = "```\n"
        embed_field += "%-15s: %.2fCV, %.0f%%RV\n" % (
            character_name,
            self.characters[character_name]["CV"],
            self.characters[character_name]["RV"]
        )
        embed_field += "```"
        new_embed = discord.Embed()
        new_embed.add_field(name=character_name, value=embed_field)
        await interaction.response.edit_message(
            content=character_name,
            view=FullShowcaseView(self.characters, character_name),
            embed=new_embed
        )


class FullShowcaseView(discord.ui.View):
    def __init__(self, characters: tuple, active_character: str = None):
        super().__init__()
        self.add_item(SelectCharacters(characters, active_character))
