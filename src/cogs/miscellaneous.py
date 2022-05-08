from ast import alias
import discord
from discord.ext import commands
from discord.commands import Option
import random

# This is needed to import the config file from the parent directory
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve().parent))
import config

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    fun = discord.SlashCommandGroup(name="fun", guild_ids=config.BOT_COMMAND_GUILDS, description="A collection of fun commands")

    @fun.command(description="Roll a six sided die")
    async def dice(self, ctx):
        await ctx.respond(f":game_die: | {random.randint(1,6)}")
    
    @fun.command(description="Answers yes or no")
    async def yesorno(self, ctx):
        if random.randint(0,1) == 1:
            await ctx.respond("Yes")
        else:
            await ctx.respond("No")

    @discord.slash_command(guild_ids=config.BOT_COMMAND_GUILDS, description="Check if the bot is responding")
    async def ping(self, ctx):
        await ctx.respond("Pong! :smiley:")

    @discord.slash_command(guild_ids=config.BOT_COMMAND_GUILDS, description="Verify your membership")
    async def verify(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=config.BOT_VERIFIED_ROLE_NAME)
        await ctx.interaction.user.add_roles(role)
        await ctx.respond("You can now write messages in the server. Welcome to the community!", ephemeral=True)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))