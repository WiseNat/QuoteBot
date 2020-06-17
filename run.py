import discord
from discord.ext import commands

from cogs.commands import Commands


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="*", description="Quoting Time",
                         activity=discord.Activity(type=discord.ActivityType.listening, name="*help"))

    async def on_ready(self):
        print("Name:\t{0}\nID:\t\t{1}".format(super().user.name, super().user.id))

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        else:
            await ctx.send("`{0}`".format(exception))

    def run(self):
        super().run(open("token.secret", "r").read())


bot = Bot()
bot.remove_command("help")
bot.add_cog(Commands(bot))
bot.run()

