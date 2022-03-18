import asyncio
import nextcord
from nextcord.ext import commands
import random


class Gifs(commands.Cog):
    """
    Interact with others using gifs
    """

    def __init__(self, client):
        self.client = client

    @commands.command(usage="<member>", aliases=["give_hug"])
    async def hug(self, ctx, *, member):
        """
        Give someone a hug ❤️
        """
        await ctx.send(f"{member}, did you need a hug? Sadly, the hug feature is not available on this version.")

    @commands.command(aliases=["murder", "stab", "mutilate", "crucify", "decapitate"])
    async def kill(self, ctx, *, member):
        """
        Kill your enemies.
        """
        await ctx.send("The kill feature is disabled on this version.")

    @commands.command(aliases=["bully"])
    async def shit_on(self, ctx, *, member):
        """
        Screw that guy.
        """
        if member.lower() == "praxis":
            for _ in range(3):
                await asyncio.sleep(3)
                await ctx.send("Fuck Praxis!")
        else:
            await ctx.send("The bully feature is disabled on this version unless the target is praxis.")


def setup(client):
    client.add_cog(Gifs(client))
