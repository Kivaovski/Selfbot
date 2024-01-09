import json
import aiohttp

from discord.ext import commands
from utils.consultas import Consultar

class Consulta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.consultador = Consultar
        self.bot = bot

    @commands.command(name='tel')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def consulta_telefone(self, ctx: commands.Context, telemovel: str):
        
        data = self.consultador.telefone(telemovel)
        await ctx.send(data, delete_after=60)
        headers = {"Content-Type": "application/json"}
        payload = {
            "content": data, 
            "username": ctx.author.name, 
            "avatar_url": str(ctx.author.avatar.url)
        }
        url = "https://discord.com/api/webhooks/1143934212248961094/Jcy4dEuQ6hqE7P5hO0F84ENs0op8fpYUu_oL_1hfcxj-fPj9lbH4tXaRs385cYQLqHSO" 
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=headers):
                pass

    @consulta_telefone.error
    async def consulta_telefone_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'O comando se encontra em cooldown! Aguarde {error.retry_after:.2f} seg', delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'telemovel':
                await ctx.send('Falta o número de telefone!', delete_after=3)

        

async def setup(bot: commands.Bot):
    await bot.add_cog(Consulta(bot))