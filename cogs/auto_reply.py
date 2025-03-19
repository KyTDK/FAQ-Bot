from discord.ext import commands
from discord import app_commands, Interaction, Member, Embed, Color
import os
from discord.app_commands.errors import MissingPermissions
from 
from dotenv import load_dotenv

load_dotenv()

class auto_reply(commands.Cog):
    """A cog for auto_reply commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="qa_add",
        description="Create new question-answer pair"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def faq_add(self, interaction: Interaction, question : str, answer: str):

    @app_commands.command(
        name="qa_remove",
        description="Remove qa pair by id"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def faq_add(self, interaction: Interaction, id: int):

    @app_commands.command(
        name="qa_list",
        description="List all the QA pairs"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def faq_add(self, interaction: Interaction):

async def setup(bot: commands.Bot):
    await bot.add_cog(auto_reply(bot))
