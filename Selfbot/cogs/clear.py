from discord.ext import commands
from utils.discutils import DiscUtils

import discord
import asyncio

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.discb = DiscUtils

    async def confirm_operation(self, ctx: commands.Context, opcao: str) -> bool:
        """
        Envia uma mensagem de confirmação de operação do selfbot e a retorna.
        ctx: commands.Context 
            contexto invocado
        opcao: str
            tipo do clear a ser modificado na mensagem
        Retorna:
            response: discord.Message
        caso for respondido   
        """
        option: discord.Message = await self.discb.get_input(
            self,
            texto=f'Confirma clear: **{opcao}?** É uma ação irreversível [S|N]',
            ctx=ctx,
            bot=self.bot
        )

        option = option.content.upper()

        if option == 'N':
            await ctx.send('Operação cancelada', delete_after=5)
            return False

        if option not in ['S', 'N']:
            await ctx.send('Operação cancelada devido a resposta inválida', delete_after=3)
            return False

        if option == 'S':
            return True

        return False


    @commands.group(name='clear')
    async def grupo_clear(self, ctx: commands.Context):

        if not ctx.invoked_subcommand:
            await ctx.send(f'Lista de comandos: amigos, grupos, dm, guilds, msgs', delete_after=3)

    @grupo_clear.command(name='amigos')
    async def clear_friends(self, ctx: commands.Context):
                
        operacao = await self.confirm_operation(ctx, 'amigos')

        if not operacao:
            return

        amigos = 0
        relations = self.bot.relationships

        if relations:
            for relation in relations:
                if isinstance(relation, discord.RelationshipType.friend):
                    try:
                        await relation.user.remove_friend()
                        await asyncio.sleep(2)
                        amigos += 1
                    except (discord.Forbidden, discord.HTTPException):
                        await ctx.send(f'Não foi possível remover {relation.nick}', delete_after=3)

        await ctx.send(f"```ansi\n[2;31m[2;32maaa[0m[2;31m[0mforam removidos {amigos}```")

                        
    
    @grupo_clear.command(name='grupos')
    async def clear_groups(self, ctx: commands.Context):
        
        
        operacao = await self.confirm_operation(ctx, 'grupos')

        if not operacao:
            return
    
        grupos = 0
        grupos_bot: discord.abc.PrivateChannel = self.bot.private_channels

        for grupo in grupos_bot:
            if isinstance(grupo, discord.GroupChannel):
                try:
                    await grupo.leave(silent=True)
                    await asyncio.sleep(1.3)
                    grupos += 1
                except (discord.HTTPException):
                    await ctx.send(f'Não foi possivel sair do grupo: {grupo.name}', delete_after=5)

        await ctx.send(f"```ansi\n[2;31m[2;32maaa[0m[2;31m[Sai de {grupos} grupos```")
                    

    @grupo_clear.command(name='dm')
    async def clear_dm(self, ctx: commands.Context):
        operacao = await self.confirm_operation(ctx, 'DM')

        if not operacao:
            return

        dms_num = 0
        dms = self.bot.private_channels
        for channel in dms:
            if isinstance(channel, discord.DMChannel) and isinstance(channel.recipient, discord.User):
                try:
                    await channel.close()
                    await asyncio.sleep(1.5)
                    dms_num += 1
                except (discord.HTTPException):
                    await ctx.send(f'Não foi possivel fechar DM com {channel.recipient.name}', delete_after=5)

        await ctx.send(f"```ansi\n[2;31m[2;32maaa[0m[2;31m[0mLimpou {dms_num} DMs```")

    @grupo_clear.command('guildas')
    async def clearGuildas(self, ctx: commands.Context):

        option = await self.confirm_operation(ctx, 'guildas')

        if not option:
            return
        
        servidores = self.bot.guilds

        for servidor in servidores:
            if isinstance(servidor, discord.Guild):
                try:
                    await servidor.delete()
                    await asyncio.sleep(3)
                except (discord.Forbidden, discord.HTTPException):
                    await servidor.leave()
                    await asyncio.sleep(3)

    @grupo_clear.command(name='msgs')
    async def clear_msgs(self, ctx: commands.Context, quantidade: int):

        limpas = 0
        async for message in ctx.channel.history(limit=quantidade):
            if message.author == self.bot.user:
                try:
                    await message.delete()
                    await asyncio.sleep()
                    limpas += 1
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    pass
            
        await ctx.send(f"Apaguei: {limpas} {'mensagens' if limpas > 1 else 'mensagem'}", delete_after=4)


async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))