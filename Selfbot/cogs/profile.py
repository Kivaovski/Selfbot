from discord.ext import commands
from utils.discutils import DiscUtils

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.discb = DiscUtils()

    @commands.command(name='house')
    async def house(self, ctx: commands.Context, housechoice: int):
        response = await self.discb.change_hypehouse(house=housechoice, token=self.bot.http.token)
        await ctx.send(response, delete_after=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
