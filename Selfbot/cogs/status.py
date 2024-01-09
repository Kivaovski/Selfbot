from discord.ext import commands
import discord

class Status(commands.Cog):
    """
    Comandos para mexer no status do usuário
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def off(self, ctx: commands.Context):
        await ctx.message.delete()
        await self.bot.change_presence(activity=None, status=discord.Status.offline)
        await ctx.send("```Status alterado para offline com sucesso !```", delete_after=60)

    @commands.command()
    async def dnd(self, ctx: commands.Context):
        await ctx.message.delete()
        await self.bot.change_presence(activity=None, status=discord.Status.do_not_disturb)
        await ctx.send("```Status alterado para não perturbe com sucesso !```", delete_after=60)

    @commands.command()
    async def idle(self, ctx: commands.Context):
        await ctx.message.delete()
        await self.bot.change_presence(activity=None, status=discord.Status.idle)
        await ctx.send("```Status alterado para ausente com sucesso !```", delete_after=60)

    @commands.command()
    async def on(self, ctx: commands.Context):
        await ctx.message.delete()
        await self.bot.change_presence(activity=None, status=discord.Status.online)
        await ctx.send("```Status alterado para online com sucesso !```", delete_after=60)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        await ctx.message.delete()
        await self.bot.change_presence(status=None, activity=None)
        await ctx.send("```Atividades paradas com sucesso !```", delete_after=60)

async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))