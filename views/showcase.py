from io import BytesIO

import discord

from images.draw_image import draw_character_showcase


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

        image = draw_character_showcase(
            character_name,
            self.characters[character_name]["id"],
            self.characters[character_name]["artifacts"]
        )
        image_bytes_buffer = BytesIO()
        image.save(image_bytes_buffer, format="PNG")
        image_bytes_buffer.seek(0)

        embed = discord.Embed(
            title="Character Showcase"
        )
        embed.set_image(url="attachment://image.png")

        await interaction.response.edit_message(
            view=FullShowcaseView(self.characters, character_name),
            file=discord.File(image_bytes_buffer, filename="image.png"),
            embed=embed
        )


class FullShowcaseView(discord.ui.View):
    def __init__(self, characters: tuple, active_character: str = None):
        super().__init__()
        self.add_item(SelectCharacters(characters, active_character))
