import discord
from discord.ext import commands
from discord.commands import Option
import rcon.source

from mojang import MojangAPI
from mcstatus import JavaServer

# This is needed to import the config file from the parent directory
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve().parent))
import config

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    minecraft = discord.SlashCommandGroup(name="mc", guild_ids=config.BOT_COMMAND_GUILDS, description="Minecraft utility commands")

    @minecraft.command(description="Get information about a minecraft player")
    async def player(
        self,
        ctx,
        playername: Option(str, "Player to lookup")
    ):
        try:
            uuid = MojangAPI.get_uuid(playername)
            playername = MojangAPI.get_username(uuid)
            nameHistory = MojangAPI.get_name_history(uuid)
            playerImageURL = "https://crafatar.com/renders/body/" + uuid
            nameHistoryStr = ""

            for name in nameHistory:
                nameHistoryStr += name["name"] + "\n"

            embed = discord.Embed(
                title=f"Minecraft player {playername}:",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=playerImageURL)
            embed.add_field(name="UUID:", value=uuid, inline=False)
            embed.add_field(name="Name history (old to new):", value=nameHistoryStr)
            await ctx.respond(embed=embed)

        except: # API could not find player or previous step failed
            await ctx.respond(":warning: | Could not find the specified player.", ephemeral=True)

    @minecraft.command(description="Get server status")
    async def status(
        self,
        ctx,
        address: Option(str, "Server address")
    ):
        try:
            mcServer = JavaServer.lookup(address)
            mcStatus = mcServer.status()
        except:
            await ctx.respond(":warning: | Could not connect to the specified server!")
        
        if (mcStatus != None):

            embed = discord.Embed(
                title=f"Minecraft server:",
                color=discord.Color.green()
            )
            embed.add_field(name="Address:", value=address, inline=False)
            embed.add_field(name="Players online:", value=f"{mcStatus.players.online}/{mcStatus.players.max}", inline=False)
            embed.add_field(name="MOTD:", value=mcStatus.description, inline=False)
            await ctx.respond(embed=embed)

    @minecraft.command(description="Add a player to the minecraft server whitelist")
    async def whitelist(
        self,
        ctx,
        playername: Option(str, "Player to whitelist")
    ):
        try:
            playerUUID = MojangAPI.get_uuid(playername)
            playerUsername = MojangAPI.get_username(playerUUID)

            if playerUsername != None:
                # Try connecting to RCON and executing commands
                with rcon.source.Client(config.MC_RCON_HOST, config.MC_RCON_PORT, passwd=config.MC_RCON_PASSWORD) as c:
                    c.run(f"whitelist add {playerUsername}")
                    
                embed = discord.Embed(
                title=f"{playerUsername} is now whitelisted!",
                description=f"{ctx.interaction.user.mention} has added `{playerUsername}` to the whitelist.",
                color=discord.Color.green()
                )
                embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playerUUID}")
                await ctx.respond(embed=embed)
            else:
                raise Exception("The player does not exist!")

        except:
            await ctx.respond(":warning: | Could not whitelist the player.", ephemeral=True)

def setup(bot):
    bot.add_cog(Minecraft(bot))