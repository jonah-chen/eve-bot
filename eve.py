import asyncio
import datetime
from urllib.request import urlopen
import ssl
import nextcord
from nextcord.ext import commands
import os
import pytz
import random
import time
from dotenv import load_dotenv
load_dotenv()

class Eve:
    def __init__(self):
        self.client = commands.Bot(command_prefix=["eve ", "Eve "], case_insensitive=True, help_command=None)
        self.praxis = dict()
        self.bme = dict()


    def main(self):
        @self.client.event  # Cuz client holds instance of Bot
        async def on_ready():  # When the bot has everything it needs and is ready
            await self.client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="with her sister Lilith"))
            print("Eve, online and ready!")


        @self.client.command()
        async def help(ctx):
            help_embed = nextcord.Embed(
                title = "List of Commands",
                description = "To see a full list of my commands and how to use them, please refer to my personal webpage: \nhttps://charles-yuan.netlify.app/eve.html",
                colour = 0x0adbfc
            )
            help_embed.set_author(name="Forked from Chubbyman2", icon_url="https://avatars.githubusercontent.com/u/70110720?s=400&u=ce8fccea831f916059794c992dd0ce1a3e77ac2c&v=4")
            help_embed.set_thumbnail(url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
            help_embed.set_footer(text="Github: https://github.com/Chubbyman2/eve-bot")
            help_embed.add_field(name="General/Admin Commands", value="```help - Displays this message \nclear - Clears a specified number of preceding lines \
                \nkick - Kicks a specified user \nban - Bans a specified user \nunban - Unbans a specified user \nload - Loads a specified cog \
                \nunload - Unloads a specified cog \npoke - Sends a dm to a specified user with your user signature \
                \ngive_flowers - Sends flowers to a specified user \npm - Sends a private message to a specified user \
                \napm - Sends an anonymous private message to a specified user \
                \nhowweeb - How much of a weeb are you? \nhyperactive - Unleashes Eve's hyperactive skill: Odin Spear```", inline=False)
            help_embed.add_field(name="Cog Commands", value="```8ball - Ask Eve a random yes/no question, and she will reply from a list of responses \
                \nyoutube - Eve will return the first video she finds on Youtube given a query \nneko - Returns a picture of a neko \
                \nwiki - Returns the first 3 sentences of the Wikipedia entry given a query \nhug - Sends a gif of a hug to a specified user \
                \nkill - Sends a gruesome gif of a death to a specified user \nshit_on - Eve will insult the specified user \
                \ndefine - Returns the definition(s) of a word if found```", inline=False)
            help_embed.add_field(name="Project Management", value="```toggle_live - Toggle live reminders and updates on or off \
                \ntodo - Displays the TODO list for all the incomplete events scheduled for the future \
                \ndescribe - Display the details of the specified event/task \
                \nassign - Assigns a specified event/task to a specified user \
                \nadd_task - Adds a task to the TODO list \
                \nadd_desc - Adds a description to the specified event/task \
                \ncat - Adds an event to a specified category \
                \ndue - Sets the due date of the specified event/task \
                \nremind - Set how long before the due date to send the users assigned a reminder \
                \ndone - Marks an event as complete```", inline=False)
            help_embed.add_field(name="Skynet Commands", value="```passcode - 'Sarah Connor' \nlock - Forces the passcode to be re-entered. Can only be used by my master \
                \nadmin_lock - Completely locks down Skynet commands. Can only be unlocked by my master \nskynet_list - Displays a list of Skynet commands \
                \nlist_cities - Returns a list of all the cities available for nuking \nskynet - Nukes a specified city(s) from the list \
                \nskynet_all - Nukes all the cities on the list \nskynet_purge - Continuously nukes all the cities on the list until there are no survivors```", inline=False)
            await ctx.send(embed=help_embed)


        @self.client.command()
        async def load(ctx, extension):  # The extension is the cog you wish to load
            self.client.load_extension(f"cogs.{extension}")
            print("Cog has been successfully loaded.")
            if extension == "nuke":
                await ctx.send("Nuke loaded.")


        @self.client.command()
        async def unload(ctx, extension):
            self.client.unload_extension(f"cogs.{extension}")
            print("Cog has been successfully unloaded.")


        @self.client.event
        async def on_member_join(member):
            print(f"{member} has joined the server.")


        @self.client.event
        async def on_member_remove(member):
            print(f"{member} has left the server.")


        @self.client.command()
        async def kick(ctx, member: nextcord.Member, *, reason=None):
            await member.kick(reason=reason)


        @self.client.command()
        async def ban(ctx, member: nextcord.Member, *, reason=None):
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.mention}")
        

        @self.client.command()
        # Can't do nextcord.Member, because it can't convert a string to a member object
        async def unban(ctx, *, member):
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")  # Splits account name at #

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}.")
                    return


        @self.client.event
        async def on_message(message):
            message_content = message.content.lower()
            message_content = message_content.split()

            if message.content == "test":
                msg = "Test successful."
                await message.channel.send(msg)

            # Unloads the nuke cog so unwitting admins don't see it 
            if "eve help" in message.content:
                try:
                    self.client.unload_extension("cogs.nuke")
                except:
                    pass
            
            await self.client.process_commands(message) # The magic command
        

        @self.client.command()
        async def test(ctx):
            await ctx.send("Test successful.")


        @self.client.command()
        async def poke(ctx, member: nextcord.Member = None):
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f"{ctx.author.name} poked you!")
            else:
                await ctx.send("Please use @mention to poke someone")

        
        # Private message
        @self.client.command()
        async def pm(ctx, member: nextcord.Member = None, *, message):
            print(f"{ctx.author.name} has PMed {member.name}")
            print(f"member is {member}")
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f'{message}\n-{ctx.author.name}')
            else:
                await ctx.send("Please use @mention to message someone")


        # Anonymous private message
        @self.client.command()
        async def apm(ctx, member: nextcord.Member = None, *, message):
            if member is not None:
                channel = member.dm_channel
                if channel is None:
                    channel = await member.create_dm()
                await channel.send(f'{message}')
            else:
                await ctx.send("Please use @mention to message someone")

        @self.client.command()
        async def hyperactive(ctx):
            await ctx.send("Hyperactive is not supported on the current version.")

        @self.client.command(aliases=["delete", "del", "remove"])
        async def clear(ctx, amount=10):  # Clears a specified number of lines
            await ctx.channel.purge(limit=amount)


        # Gives flowers
        @self.client.command(aliases=["give_flower", "give_rose", "give_roses", "send_flower", "send_flowers", "send_roses", "send_rose"])
        async def give_flowers(ctx, member):
            await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved {ctx.author}.")

        
        @self.client.command(aliases=["howeeb"])
        async def howweeb(ctx):
            await ctx.send(f"According to my calculations, you are {round(random.gauss(50, 50), 1)}% weeb.")


        # Every hour, Eve will send the message "Fuck Praxis"
        @self.client.command()
        async def fuck_praxis(ctx):
            EST = pytz.timezone("US/Eastern")
            id = ctx.author.guild.id
            if id in self.praxis:
                self.praxis[id] = not self.praxis[id]
            else:
                self.praxis[id] = True

            praxis_time = datetime.datetime.now(EST).strftime("%H:%M:%S")
            await ctx.send(f"Praxis bullying has {'commenced' if self.praxis[id] else 'been stopped'} at {praxis_time} EST.")

            while self.praxis[id]:
                await ctx.send(":regional_indicator_f: :regional_indicator_u: :regional_indicator_c: :regional_indicator_k: " +\
                    ":regional_indicator_p: :regional_indicator_r: :regional_indicator_a: :regional_indicator_x: :regional_indicator_i: :regional_indicator_s:")
                # Asyncio is useful because it allows other tasks to be run while .sleep() is active
                await asyncio.sleep(3600)
        
        @self.client.command()
        async def fuck_bme(ctx):
            BME = "<div class=\"RatingValue__Numerator-qw8sqy-2 liyUjw\">"
            ssl._create_default_https_context = ssl._create_unverified_context

            EST = pytz.timezone("US/Eastern")
            id = ctx.author.guild.id
            if id in self.bme:
                self.bme[id] = not self.bme[id]
            else:
                self.bme[id] = True

            bme_time = datetime.datetime.now(EST).strftime("%H:%M:%S")
            await ctx.send(f"BME bullying has {'commenced' if self.bme[id] else 'been stopped'} at {bme_time} EST.")

            while self.bme[id]:
                bme_time = datetime.datetime.now(EST).strftime("%H:%M:%S")
                page = urlopen("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2479393")
                page = page.read()
                page = page.decode("utf-8")
                rating_start = page.find(BME) + len(BME)
                rating_end = page.find("</div>", rating_start)
                rating = page[rating_start:rating_end]
                await ctx.send(":regional_indicator_f: :regional_indicator_u: :regional_indicator_c: :regional_indicator_k: " +\
                    ":regional_indicator_b: :regional_indicator_m: :two: :zero: :five:\n" +\
                        f"The Prof Rating is currently {rating}/5 (last updated on {bme_time} EST).")
                # Asyncio is useful because it allows other tasks to be run while .sleep() is active
                await asyncio.sleep(3600)

        
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                # Cuts cog_example.py to cog_example
                self.client.load_extension(f"cogs.{filename[:-3]}")
        
        # Yes, order matters; you have to run this last
        TOKEN = os.environ["TOKEN"]
        self.client.run(TOKEN)


if __name__ == "__main__":
    eve = Eve()
    eve.main()
    
