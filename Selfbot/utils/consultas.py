import aiohttp

from bs4 import BeautifulSoup

class Consultar:
    """
    Classe das consultas do iFind
    """
    def __init__(self):
        self.query_type = None
        self.base_url = f"http://localhost:1337/consultar/{self.query_type}/"
        self.session = aiohttp.ClientSession()

    async def telefone(self, tel: str):
        data = {"tipo": "iFind", "Tel": tel}
        self.query_type = "Telefone"
        
        async with self.session.post(self.base_url, data=data) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                error_heading = soup.find('h1', class_='titleConsulta')
                if error_heading and error_heading.text.strip() == 'Erro':
                    return "Não foi encontrado na base de dados"
                table = soup.find("table", class_="dataframe")
                data = {}
                for row in table.find_all("tr"):
                    th: str = row.find("th")
                    td: str = row.find("td")
                    if th and td:
                        data[th.text.strip()] = td.text.strip()
                data_string = ""
                for key, value in data.items():
                    data_string += f"{key}: {value}\n"
                return data_string
            else:
                return "Tivemos um erro ao consultar!"

    async def close(self):
        await self.session.close()

async def setup(bot):
    await bot.add_cog(Consultar(bot))