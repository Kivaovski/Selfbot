import re

from discord.ext import commands
from utils.discutils import DiscUtils
import discord
class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.discb = DiscUtils
        self.bot = bot
        self._last_result = None

    @commands.command()
    async def ceo(self, ctx: commands.Context):
        await ctx.message.delete()
        msg = "```Desenvolvido por equipe WannaCry```"
        await ctx.send(msg, delete_after=5)

    @commands.command()
    async def help(self, ctx: commands.Context):
        msg = self.discb.load_help()
        await ctx.send(msg, delete_after=60)

    @commands.command()
    async def suporte(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send("https://discord.gg/wannacry", delete_after=8)

    @commands.command()
    async def info(self,ctx, member: commands.MemberConverter = None):
        await ctx.message.delete()
        if member != None:
            name = member.name
            nick = member.nick
            user_id = member.id
            discriminator = member.discriminator
            mention = member.name
            status = member.status
            activity = member.activity
            created_at = member.created_at
            avatar_url = member.avatar
            flags = str(member.public_flags.all())

            flags = re.findall(r"<UserFlags.(.*?):", flags)
            flags = ", ".join(flags)

            if member.is_on_mobile():
                plataforma = "Mobile"
            elif member.desktop_status:
                plataforma = "Desktop"
            
            info_message = f"""
    # Informações de {mention}\n
    **Nome:** ```ansi\n[2;32m{name}[0m```
    **Apelido:** ```ansi\n[2;32m{nick}[0m```
    **ID:** ```ansi\n[2;32m{user_id}[0m```
    **Discriminador:** ```ansi\n[2;32m{discriminator}[0m```
    **Status:** ```ansi\n[2;32m{status}[0m```
    **Atividade:** ```ansi\n[2;32m{activity}[0m```
    **Criado em:** ```ansi\n[2;32m{created_at}[0m```
    **Avatar:** ```ansi\n[2;32m{avatar_url}[0m```
    **Plataforma:** ```ansi\n[2;32m{plataforma}[0m```
    **Insignias:** ```ansi\n[2;32m{flags}[0m```
            """
            await ctx.send(info_message, delete_after=60)
        else:
            await ctx.send("coloque a pessoa que quer consultar!")



async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
