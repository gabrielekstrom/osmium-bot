import discord
from discord.commands import Option
import config

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have successfully logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="the chat!", type=discord.ActivityType.watching))

# Load cogs
bot.load_extension('cogs.minecraft')
bot.load_extension('cogs.moderation')
bot.load_extension('cogs.miscellaneous')

# Run the bot
bot.run(config.BOT_TOKEN)