import os

import asyncio

from discord.ext import commands
from utils.discutils import DiscUtils


class WannaCry(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.config = DiscUtils.load_config()
        self.cogs_fcking_nams = None
        super().__init__(*args, **kwargs)

    async def load_cogs(self, pasta: str):
        """
        Carrega os comandos|modulos do Bot
        """
        for filename in os.listdir(pasta):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'{pasta[0:]}.{filename[:-3]}')
                except Exception as e:
                    print(e, filename, 'not loaded')
        
    async def reload_cogs(self, pasta: str):
        """
        Recarrega os comandos|modulos do Bot
        """
        for filename in os.listdir(pasta):
            if filename.endswith('.py'):
                try:
                    await self.reload_extension(f'{pasta[0:]}.{filename[:-3]}')
                except Exception as e:
                    print(e, filename, 'not reloaded')
    async def on_ready(self):
        print(f"Logged in as {self.user.name} | {self.user.id}")
        await self.change_presence(activity=None)
        await self.load_cogs('cogs')

    async def online(self):
        await self.start(self.config['token'])


async def main():
    conf = DiscUtils.load_config()
    bot = WannaCry(
        command_prefix=conf['prefixo'],
        help_command=None,
        self_bot=True  
    )
    

    @bot.command(name='rl')
    async def recar(ctx: commands.Context):
        if ctx.author.id in [1105631378390925464, 752311109226201101]:
            """
            Recarrega cogs
            Se for reescrever codigo na cogs so rode este comando!
            """
            await bot.reload_cogs(pasta='cogs')
            em = ':white_check_mark: '
            await ctx.reply(f'**[{em}]** Cogs recarregadas!')
            return
        
        await ctx.send('Não é dev!')


    await bot.online()

if __name__ == '__main__':
    asyncio.run(main())