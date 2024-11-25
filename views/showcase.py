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
        await interaction.response.edit_message(content="Working on it...")
        image = draw_character_showcase(
            character_name,
            self.characters[character_name]["avatarInfo"],
            self.characters[character_name]["player_uid"]
        )
        image_bytes_buffer = BytesIO()
        image.save(image_bytes_buffer, format="PNG")
        image_bytes_buffer.seek(0)

        embed = discord.Embed(
            title="Character Showcase"
        )
        embed.set_image(url="attachment://image.png")
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            view=FullShowcaseView(self.characters, character_name),
            file=discord.File(image_bytes_buffer, filename="image.png"),
            content=None,
            embed=embed
        )


class FullShowcaseView(discord.ui.View):
    def __init__(self, characters: tuple, active_character: str = None):
        super().__init__()
        self.add_item(SelectCharacters(characters, active_character))
