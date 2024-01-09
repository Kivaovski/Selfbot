import sys
import json
import random
import requests

import asyncio
import aiohttp
import discord


from discord.ext.commands import Context, Bot

class DiscUtils:
    def __init__(self):
        pass
    
    def hidden_exp_msg(visible: str, hidden: str) -> str:
        return visible + ("||\u200b||" * 200) + hidden
    
    async def get_input(ctx: Context, bot: Bot, texto: str) -> discord.Message:
        """
        Envia uma mensagem com e aguarda mensagem do selfbot e a retorna.

        ctx: commands.Context 
            contexto invocado
        bot: commands.Bot
            selfbot
        text: str
            mensagem a ser enviada
        Retorna:
            response: discord.Message
        caso for respondido          
        """
        def check(message: discord.Message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            await ctx.send(texto, delete_after=15)
            response = await bot.wait_for("message", check=check, timeout=60)
            return response
        except asyncio.TimeoutError:
            return None

    @classmethod
    def geek(self, token=None):
        """
        Retorna um cabeçalho HTTP com um token de autorização opcional.

        Argumentos:
            token: str, opcional
                -- Token de autorização para ser adicionado ao cabeçalho.

        Retorna:
            headers: dict
                -- Dicionário contendo os cabeçalhos HTTP.
        """ 
        self.heads: list[dict[str, str]] = [{
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
        }]  
        headers = random.choice(self.heads)
        if token:
            headers.update({"Authorization": token})    
            return headers
    
    @staticmethod
    async def change_hypehouse(house: int, token: str):
        if house not in [1, 2, 3]:
            return "Favor, verifique de escolher entre 1, 2 ou 3."

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0",
        }
        
        data = {"house_id": house}
        
        async with aiohttp.ClientSession as session:
            async with session.post("https://discord.com/api/v9/hypesquad/online", json=data, headers=headers) as response:
                if response.status in [200, 204]:
                    return "Sucesso! Veja seu perfil."
                else:
                    return "Algum erro aconteceu. Contate os desenvolvedores!"


    @classmethod
    def load_help(self) -> str:
        """
        Retorna:
            txt: str
                -- O conteúdo do arquivo de texto.
        """
        with open('help.txt', 'r', encoding='utf-8') as f:
            txt = f.read()
        return txt
    
    @classmethod
    def load_config(self):
        """
        Carrega a configuração de um arquivo JSON com base no ID fornecido como argumento de linha de comando.

        Retorna:
            conf: dict
                -- Um dicionário contendo a configuração carregada.
        """
        id = sys.argv[1]
        with open(f"configs//{id}.json", "r") as file:
            conf = json.loads(file.read())
        return conf
    
    @classmethod
    def write_config(self, attribute, value):
        """
        Escreve um valor em um atributo específico do arquivo de configuração JSON.

        Argumentos:
            attribute: str
                -- O nome do atributo a ser atualizado.
            value: any
                -- O valor a ser atribuído ao atributo especificado.
        """
        id = sys.argv[1]
        self.config = self.load_config()

        if attribute == "custom_status":
            self.config[attribute] = not self.config.get(attribute, False)
        else:
            self.config[attribute] = value

        with open(f"configs//{id}.json", 'w') as file:
            json.dump(self.config, file, indent=4)

    def clear(token: str):
        custom_status = {"custom_status": {"text": None}}
        return requests.patch("https://discord.com/api/v9/users/@me/settings", headers=token, json=custom_status)
