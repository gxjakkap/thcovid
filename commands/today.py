import requests
import nextcord
from commands.base_command import BaseCommand


class today(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "รายงานสถานการณ์ COVID-19 ประจำวัน"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        url = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-all'
        r = requests.get(url)
        ans = r.json()
        updated_text = f"{ans[0]['update_date']} GMT+7"
        embed = nextcord.Embed(title="รายงานสถานการณ์ COVID-19 ประจำวัน")
        embed.add_field(name="🚑เคสใหม่",
                        value=f"{ans[0]['new_case']:,}", inline=False)
        embed.add_field(name="🚑เคสใหม่ (ยกเว้นเดินทางจากต่างประเทศ)",
                        value=f"{ans[0]['new_case_excludeabroad']:,}", inline=False)
        embed.add_field(name="🏥เคสสะสม",
                        value=f"{ans[0]['total_case']:,}", inline=False)
        embed.add_field(name="🏥เคสสะสม (ยกเว้นเดินทางจากต่างประเทศ)",
                        value=f"{ans[0]['total_case_excludeabroad']:,}", inline=False)
        embed.add_field(name="🪦เสียชีวิต",
                        value=f"{ans[0]['new_death']:,}", inline=False)
        embed.add_field(name="🪦เสียชีวิตสะสม",
                        value=f"{ans[0]['total_death']:,}", inline=False)
        embed.add_field(name="🌼หายป่วยวันนี้",
                        value=f"{ans[0]['new_recovered']:,}", inline=False)
        embed.add_field(name="🌼หายป่วยสะสม",
                        value=f"{ans[0]['total_recovered']:,}", inline=False)
        embed.add_field(name="📅ข้อมูลอัปเดตล่าสุด",
                        value=updated_text, inline=False)
        embed.set_footer(text="ข้อมูลจาก covid19.ddc.moph.go.th")
        # await asyncio.gather(message.author.mention, message.channel.send(embed=embed))
        await message.channel.send(message.author.mention)
        await message.channel.send(embed=embed)
