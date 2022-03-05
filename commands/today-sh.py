import requests
import nextcord
from datetime import datetime
from commands.base_command import BaseCommand


class todaysh(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "รายงานสถานการณ์ COVID-19 ประจำวัน"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        url = 'https://disease.sh/v3/covid-19/countries/th?strict=true'
        r = requests.get(url)
        ans = r.json()
        time = int(ans['updated'])/1000
        updated = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        updated_text = f'{updated} UTC'
        embed = nextcord.Embed(title="รายงานสถานการณ์ COVID-19 ประจำวัน")
        embed.add_field(name="🚑เคสใหม่",
                        value=f"{ans['todayCases']:,}", inline=False)
        embed.add_field(name="🏥เคสสะสม",
                        value=f"{ans['cases']:,}", inline=False)
        embed.add_field(name="🪦เสียชีวิต",
                        value=f"{ans['todayDeaths']:,}", inline=False)
        embed.add_field(name="🪦เสียชีวิตสะสม",
                        value=f"{ans['deaths']:,}", inline=False)
        embed.add_field(name="🌼หายป่วยวันนี้",
                        value=f"{ans['todayRecovered']:,}", inline=False)
        embed.add_field(name="🌼หายป่วยสะสม",
                        value=f"{ans['recovered']:,}", inline=False)
        embed.add_field(name="📅ข้อมูลอัปเดตล่าสุด",
                        value=updated_text, inline=False)
        embed.set_footer(text="ข้อมูลจาก disease.sh")
        # await asyncio.gather(message.author.mention, message.channel.send(embed=embed))
        await message.channel.send(message.author.mention)
        await message.channel.send(embed=embed)
