import datetime
import random

import discord
from discord.ext import commands


def random_date(start, end):
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("----------\nLogged in as:\n{0}\n{1}\n----------".format(self.bot.user.name, self.bot.user.id))

    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, *args):
        await ctx.message.delete()

        main_embed = discord.Embed(title="__**Help Commands**__", colour=0x00ff00)
        main_embed.add_field(name="**Command Help**",
                             value="Remind me to do stuff here. Also *execute <code>, *settings and *help are all the "
                                   "current commands",
                             inline=False)
        help_message = await ctx.send(embed=main_embed)

        await help_message.add_reaction("<:cross:671116183780720670>")

        def check(reaction, user, *args):
            return str(reaction) == "<:cross:671116183780720670>" and str(reaction.message) == str(
                help_message) and user != reaction.message.author

        await self.bot.wait_for("reaction_add", check=check)
        await help_message.delete()

    @commands.command(name="quote", aliases=["q"])
    async def quote(self, ctx, quote_channel, *args):
        """
        :param quote_channel: The channel the user wants a quote from
        :param ctx: Discord Context class

        :var latest_message: The most recent message in the desired channel
        :var oldest_message: The oldest message in the desired channel
        """
        await ctx.message.delete()

        latest_message = await ctx.channel.history(limit=1).flatten()
        oldest_message = await ctx.channel.history(limit=1, oldest_first=True).flatten()

        while True:
            date = random_date(oldest_message[0].created_at, latest_message[0].created_at)

            quotes = await ctx.channel.history(limit=50, around=date).flatten()
            try:
                message = random.choice(quotes).content
                await ctx.send(message)
                break
            except Exception as error:
                print(error)


quoter = commands.Bot(command_prefix="*", description="Quoting time")
quoter.remove_command("help")
quoter.add_cog(MainCog(quoter))
quoter.run(open("token.secret", "r").read())
