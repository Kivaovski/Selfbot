import os
import json
import base64
import threading

import asyncio
import requests

from discord.ext import commands
from firewall import firewall

from utils.discutils import DiscUtils

bot = commands.Bot(command_prefix='!', self_bot=True, help_command=None)
folder_nome = 'configs\\' if os.name == 'nt' else 'configs/'

@bot.event
async def on_command_error(ctx, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        pass



@bot.command()
async def resetar(ctx: commands.Context):
    files = [os.path.splitext(file)[0] for file in os.listdir(folder_nome) if os.path.isfile(os.path.join(folder_nome, file))]
    for file in files:
        await asyncio.create_task(async_process(contaID=file))
    await ctx.message.add_reaction('✅')

@bot.command()
async def adduser(ctx: commands.Context, token: str=None):
    await ctx.message.delete()
    token = token or bot.http.token
    if len(token) > 65:
        s = requests.Session()
        response = s.get("https://discord.com/channels/@me", headers=DiscUtils.geek(token))
        if response.status_code == 200 or response.status_code == 201:
            partes = token.split('.')
            contaID = partes[0].strip()
            quantidadeIguaisEmFalta = 4 - (len(contaID) % 4)
            if quantidadeIguaisEmFalta < 4:
                contaID += '=' * quantidadeIguaisEmFalta
            contaID = base64.b64decode(contaID)
            contaID = contaID.decode('utf-8')
            nome_arquivo = folder_nome + contaID + ".json"
            if os.path.isfile(nome_arquivo):
                with open(nome_arquivo, 'r') as f:
                    config = json.load(f)
                    config['token'] = token
                with open(nome_arquivo, 'w') as f:
                    json.dump(config, f, indent=4)
            else:
                config = {
                    "prefixo": "!",
                    "estadoStatus": 0,
                    "emoji_on_mention": False,
                    "emoji": "",
                    "cycle_list": [],
                    "custom_status": False,
                    "stream": False,
                    "token": token
                }
                with open(nome_arquivo, 'w') as f:
                    json.dump(config, f, indent=4)
            asyncio.create_task(async_process(contaID=contaID))
        else:
            await ctx.send("token direito pf....")
    else:
        await ctx.send("token direito pf....")
async def async_process(contaID):
    await asyncio.create_subprocess_shell(f"python self.py {contaID}")
firewallthread = threading.Thread(target=firewall)
firewallthread.start()
bot.run("ODUyNzY3OTQ1ODU0NTUwMDU2.GKy302.XCVWBm-WX4Pcj6UZABDPmoZKhFG3LNJ8_6CV8s")