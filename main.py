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

        main_embed = discord.Embed(title="__**Help Commands**__", description="Just do *quote #channel or *q #channel",
                                   colour=0x00ff00)
        help_message = await ctx.send(embed=main_embed)

        await help_message.add_reaction("<:cross:671116183780720670>")

        def check(reaction, user, *args):
            return str(reaction) == "<:cross:671116183780720670>" and str(reaction.message) == str(
                help_message) and user != reaction.message.author

        await self.bot.wait_for("reaction_add", check=check)
        await help_message.delete()

    @commands.command(name="quote", aliases=["q"])
    async def quote(self, ctx, *channel_mention):
        """
        :param channel_mention: The channel the user wants a quote from (user must mention it)
        :param ctx: Discord Context class

        :var quote_channel: Channel class for the channel the user wants a quote from
        :var latest_message: The most recent message in the desired channel
        :var oldest_message: The oldest message in the desired channel
        :var date: A random datetime between the latest_message and oldest_message
        :var quotes: List of messages around date
        :var message: A random message from the quotes list
        """

        if len(channel_mention) == 0:
            quote_channel = ctx.channel
        else:
            quote_channel = self.bot.get_channel(int(channel_mention[0][2:-1]))

        latest_message = await quote_channel.history(limit=1).flatten()
        oldest_message = await quote_channel.history(limit=1, oldest_first=True).flatten()

        await ctx.message.delete()

        while True:
            date = random_date(oldest_message[0].created_at, latest_message[0].created_at)
            quotes = await quote_channel.history(limit=50, around=date).flatten()

            try:
                message = random.choice(quotes)
                if message.content == "":
                    raise ValueError

                main_embed = discord.Embed(colour=0x8292ab, description=message.content + "\n\n[Jump to message](" +
                                                                        message.jump_url + ")")
                if len(message.raw_mentions) != 0:  # Getting the last mention as the quoted user
                    user = self.bot.get_user(message.raw_mentions[-1])
                    main_embed.set_author(name=user.name, icon_url=user.avatar_url)
                else:  # If there is no @ provided in the quote
                    main_embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)

                await ctx.send(embed=main_embed)
                break

            except Exception as error:
                print(error)


quoter = commands.Bot(command_prefix="*", description="Quoting time")
quoter.remove_command("help")
quoter.add_cog(MainCog(quoter))
quoter.run(open("token.secret", "r").read())
