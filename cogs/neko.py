import nextcord
from nextcord.ext import commands
import random 


# As suggested by Amaterasu#1541
class Neko(commands.Cog):
    """
    Don't lie, you know you love catgirls
    """

    def __init__(self, client):
        self.client = client

    @commands.command(usage="", aliases=["nyaa", "meow", "mew"])
    async def neko(self, ctx):
        """
        *nya* get a picture of a neko *nya*
        """
        await ctx.send("Neko command is not supported on this version")


def setup(client):
    client.add_cog(Neko(client))
