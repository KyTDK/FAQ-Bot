import os
import logging
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from modules.auto_reply import qa

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix='/',
    description="""
    🤖 FAQ Bot - Your Automated Assistant
    ----------------------------------------
    - Automatically responds to frequently asked questions.
    - Enhances server engagement by reducing repetitive queries.
    
    🔗 GitHub Repository: [FAQ-Bot](https://github.com/KyTDK/FAQ-Bot)
    """,
    intents=intents,
)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    answer = qa.find_best_match(message, threshold=0.7)
    if answer:
        await message.reply(answer)

# --- Run the Bot ---
if __name__ == "__main__":
    bot.run(TOKEN)