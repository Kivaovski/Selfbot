from typing import Union

import discord
import asyncio
import requests
import aiohttp
import time
from discord.ext import commands, tasks
from utils.discutils import DiscUtils

class always_on(commands.Cog):

    """
    - Eventos
    - Sistema de Emoji ao mencionado
    - Sistema de Call Infinita
    - Custom Status
    - Streaming
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.discb = DiscUtils()
        self.config = self.discb.load_config()
        
        self.reaction_enabled = self.config["emoji_on_mention"]
        self.reaction_emoji = self.config["emoji"]

        self.user_ignore_emoji_reaction = set()
        self.current_status = self.bot.activity
        self.statuschanger = self.config['custom_status']
        self.statusold = None
        self.streaming_status_task.start()
        time.sleep(15)
        self.status_loop.start()

    # Eventos
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):

        mention = f"<@{self.bot.user.id}>"

        if mention in msg.content:
            # Limpar caso automencionado.
            if msg.author.id == self.bot.user.id:
                self.user_ignore_emoji_reaction = set()
            
            # Se tiver
            if self.reaction_emoji:
                if msg.author.id not in self.user_ignore_emoji_reaction:
                    try:
                        await msg.add_reaction(self.reaction_emoji)
                        self.user_ignore_emoji_reaction.add(msg.author.id)
                    except (discord.HTTPException, discord.Forbidden):
                        pass                        
                elif msg.author.id in self.user_ignore_emoji_reaction:
                    return

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        await ctx.message.delete(delay=60 if ctx.command.name == 'help' else 7)
        

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Chamado quando:
            - Membro entra na call ou (palco)
            - Membro sai da call ou (palco)
            - Membro se muta ou deixa no surdo.
            - Membro é mutado ou é deixado no surdo por um Adminstrador.
        """
        if member == self.bot.user:
            if before.channel is not None and after.channel is None and self.conectado == True:
                channel = self.bot.get_channel(int(self.canal))
                if channel and isinstance(channel, discord.VoiceChannel):
                    await channel.connect(timeout=99999999,self_deaf=True,reconnect=True)


    # Grupo de comando Call
    @commands.group()
    async def call(self, ctx: commands.Context):

        if ctx.invoked_subcommand is None:
            await ctx.send("Comandos disponíveis: join e leave", delete_after=10)
    
    # Entrar
    @call.command(name="join")
    async def joiner(self, ctx, channel_id:str=""):
        await ctx.message.delete()
        self.canal = channel_id
        channel = self.bot.get_channel(int(channel_id))
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect(timeout=99999999,self_mute=True,self_deaf=True,reconnect=True)
            self.conectado = True
            await ctx.send(f'Conectado em: {channel.name}')
        else:
            await ctx.send('Canal inválido')
            
    @call.command(name="leave")
    async def leaver(self,ctx):
        await ctx.message.delete()
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            self.conectado = False
            await ctx.send(f"Deslogou da call")
        else:
            await ctx.send("não connectado!")


    # Grupo de comando Emoji
    @commands.group()
    async def emoji(self, ctx: commands.Context):

        if ctx.invoked_subcommand is None:
            await ctx.send("Comandos disponíveis: emoji add, emoji toggle", delete_after=5)
      
    # Adicionar
    @emoji.command(name="add")
    async def add_emoji(self, ctx: commands.Context, emoji_input: discord.PartialEmoji):

        if emoji_input.is_custom_emoji():
            custom_emoji = self.bot.get_emoji(emoji_input)

            if custom_emoji:
                self.reaction_emoji = custom_emoji
                
            if not custom_emoji:
                await ctx.send("Emoji customizado não encontrado!", delete_after=6)
                return
            
        if emoji_input.is_unicode_emoji():
            self.reaction_emoji = emoji_input

    
    # Ligar/Desligar
    @emoji.command(name="toggle")
    async def toggle_emoji(self, ctx: commands.Context):
        self.config = self.discb.load_config()
        self.reaction_enabled = not self.reaction_enabled  
        self.discb.write_config("emoji_on_mention", self.reaction_enabled)  
        await ctx.send('Ativado!' if self.reaction_enabled else 'Desativado!', delete_after=3)

    # Stream
    @commands.command(name='stream')
    async def stream_command(self, ctx: commands.Context):
        self.config = self.discb.load_config()
        self.config["stream"] = not self.config.get("stream")
        self.discb.write_config("stream", self.config["stream"])
        if self.statuschanger == True:
            await ctx.send("Desligue os status custom e espere 30segundos para ativar/desligar o stream")
            return
        await ctx.send(f"Streaming status {'ativado' if self.config['stream'] else 'desativado'}.", delete_after=5)

    # Custom Status
    @commands.group()
    async def status(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Comandos: add, clear, on, off", delete_after=6)
            await ctx.send(f"""```\ncustom_status: {self.config['custom_status']}\ncycle_list: {self.config['cycle_list']}```""", delete_after=4)

    @status.command(name='on')
    async def status_on(self, ctx: commands.Context):
        self.statuschanger = True
        self.discb.write_config('custom_status', self.statuschanger)
        await ctx.send('status custom animados foram ativados', delete_after=5)

    @status.command(name='off')
    async def status_off(self, ctx: commands.Context):
        self.statuschanger = False
        self.discb.write_config('custom_status', self.statuschanger)
        await ctx.send('status custom animados foram desativados', delete_after=5)
    
    @status.command(name='add')
    async def add(self, ctx: commands.Context, *, msgs: str):
        if len(msgs) > 128:
            await ctx.send("Tem que ser menor que 129 caracteres")
            return
        self.config = self.discb.load_config()
        status_list = self.config.get('cycle_list', [])
        status_list.append(msgs)
        self.discb.write_config('cycle_list', status_list)
        await ctx.send(':white_check_mark: ', delete_after=3)

    @status.command(name='clear')
    async def clear(self, ctx: commands.Context):
        self.discb.write_config('cycle_list', [])
        self.discb.clear(token=self.bot.http.token)
        await ctx.send('Limpo')

    @tasks.loop(seconds=1)
    async def streaming_status_task(self):
        self.config = self.discb.load_config()
        if self.config['stream']  and not self.bot.activity:                
            await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Streaming(
                    name=".gg/wannacry",
                    url="https://www.youtube.com/watch?v=3YxaaGgTQYM&list=RDGMEMJQXQAmqrnmK1SEjY_rKBGA&index=9"
                )
            )
        if not self.config['stream'] and self.bot.activity.type.value == 1:
            await self.bot.change_presence(activity=None)

    @tasks.loop(seconds=10)
    async def status_loop(self):
        self.config = self.discb.load_config()
        if self.config['custom_status'] and self.statuschanger:
            status_list = self.config['cycle_list']
            if not status_list:
                return
            for statusmk in status_list:
                if self.statusold == str(statusmk):
                    continue
                try:
                    custom_status = {"custom_status": {"text": f'{statusmk}'}}
                    async with aiohttp.ClientSession(headers=self.discb.geek(self.bot.http.token)) as session:
                        async with session.patch("https://discord.com/api/v9/users/@me/settings", json=custom_status) as r:
                            if r.status == 200:
                                self.statusold = str(statusmk)
                            elif "too many 4xx response codes" in await r.text():
                                print('Many requests solver')
                                await asyncio.sleep(5)
                            else:
                                print(f'[-][STATUS ERROR][{r.status}] | {await r.text()}')
                            await asyncio.sleep(5)
                except Exception as error:
                    print(f'[-][STATUS ERROR] | {error}')

    @status_loop.before_loop
    async def before_status_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(always_on(bot))
    