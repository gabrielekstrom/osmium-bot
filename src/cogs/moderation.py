import discord
from discord.ext import commands
from discord.commands import Option

# This is needed to import the config file from the parent directory
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve().parent))
import config

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(guild_ids=config.BOT_COMMAND_GUILDS, description="Purge messages from the current text channel")
    async def purge(
        self,
        ctx,
        amount: Option(int, "Amount of messages to purge"),
        author: Option(discord.Member, "Author to purge messages from", required=False)
    ):
        if ctx.author.guild_permissions.manage_messages:
            if author == None:
                purgedMessages = await ctx.channel.purge(limit=amount)
                await ctx.respond(f"Purged {len(purgedMessages)} message(s)!", ephemeral=True)
            else:
                def is_user(m):
                    return m.author == author
                purgedMessages = await ctx.channel.purge(limit=amount, check=is_user)
                await ctx.respond(f"Purged {len(purgedMessages)} message(s) sent by {author.mention}!", ephemeral=True)
        else:
            await ctx.respond(":x: | You do not have sufficient permissions to use this command!", ephemeral=True)

    @discord.slash_command(guild_ids=config.BOT_COMMAND_GUILDS, description="Warn a user")
    async def warn(
        self,
        ctx,
        user: Option(discord.Member, "User to warn"),
        reason: Option(str, "Reason for warning", required=False)
    ):
        embed = discord.Embed(
                title=f"{user} has been warned!",
                color=discord.Color.yellow()
        )
        embed.add_field(name="Reason: ", value=f"{reason}")
        embed.add_field(name="Warned by: ", value=f"{ctx.interaction.user.mention}")
        await ctx.respond(embed=embed)

    @discord.slash_command(guild_ids=config.BOT_COMMAND_GUILDS, description="Get information about a user")
    async def userinfo(
        self,
        ctx,
        user: Option(discord.Member, "User to lookup"),
    ):
        avatar_url = str(user.display_avatar)
        embed = discord.Embed(
                title=f"Information about {user}",
                color=discord.Color.dark_gray()
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Warnings: ", value="*Coming soon!*", inline=False)
        embed.add_field(name="Server join: ", value=f"{user.joined_at.strftime('%Y-%m-%d %T')}", inline=False)
        embed.add_field(name="Account creation: ", value=f"{user.created_at.strftime('%Y-%m-%d %T')}", inline=False)
        await ctx.respond(embed=embed)
    

def setup(bot):
    bot.add_cog(Moderation(bot))