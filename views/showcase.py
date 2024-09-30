
import discord


def get_star_color(roll_value: float):
    if roll_value >= 800.0:
        return "<:purple_star:1290342830769700864>"
    if roll_value >= 700.0:
        return "<:blue_star:1290339072618926225>"
    elif roll_value >= 600.0:
        return "<:green_star:1290343084843991148>"
    elif roll_value >= 500.0:
        return "<:yellow_star:1290342127406026773>"
    elif roll_value >= 400.0:
        return "<:orange_star:1290344747361374248>"
    elif roll_value >= 300.0:
        return "<:red_star:1290343395398783068>"
    else:
        return "<:gray_star:1290343533445910611>"


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
        embed_field = "\n"
        for artifact_type in self.characters[character_name]:
            if artifact_type != "Total":
                embed_field += "%-10s: %.01fCV, %.0f%%RV" % (
                    artifact_type,
                    self.characters[character_name][artifact_type]["CV"],
                    self.characters[character_name][artifact_type]["RV"]
                )
                current_rv = (
                    self.characters[character_name][artifact_type]["RV"]
                )
                embed_field += get_star_color(current_rv) + "\n"

        embed_field += ""
        new_embed = discord.Embed()
        new_embed.add_field(name=character_name, value=embed_field)
        await interaction.response.edit_message(
            view=FullShowcaseView(self.characters, character_name),
            embed=new_embed
        )


class FullShowcaseView(discord.ui.View):
    def __init__(self, characters: tuple, active_character: str = None):
        super().__init__()
        self.add_item(SelectCharacters(characters, active_character))
