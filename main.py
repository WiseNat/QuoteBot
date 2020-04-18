import discord
from discord.ext import commands


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
    async def quote(self, ctx, *args):
        """
        :param ctx: Discord Context class
        :var varName: description
        """

        await ctx.message.delete()


quoter = commands.Bot(command_prefix="*", description="Quoting time")
quoter.remove_command("help")
quoter.add_cog(MainCog(quoter))
quoter.run(open("token.secret", "r").read())
