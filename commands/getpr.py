import requests
import discord
from commands.base_command  import BaseCommand
from utils import checkprovincevalidity

class gbp(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "รายงานสถานการณ์ COVID-19 ประจำวันของแต่ละจังหวัด"
        params = ["province"]
        super().__init__(description, params)

    
    async def handle(self, params, message, client):
        url = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces'
        r = requests.get(url)
        r.encoding = 'utf-8'
        ans = r.json()
        if len(params)>1:
            usrinput = ' '.join(params)
        else:
            usrinput = params[0]
        pr = checkprovincevalidity(usrinput)
        if not pr[0]:
            await message.channel.send("Invalid province")
            exist = False
        else:
            i = 0
            while i<77:
                if ans[i]['province']==pr[1]:
                    exist = True
                    break
                else:
                    i+=1
        if exist:
            embed=discord.Embed(title="สถานการณ์ COVID-19 จังหวัด"+ans[i]['province'])
            embed.add_field(name="🚑เคสใหม่", value=f"{ans[i]['new_case']:,}", inline=False)
            embed.add_field(name="🚑เคสใหม่ (ยกเว้นเดินทางจากต่างประเทศ)", value=f"{ans[i]['new_case_excludeabroad']:,}", inline=False)
            embed.add_field(name="🏥เคสสะสม", value=f"{ans[i]['total_case']:,}", inline=False)
            embed.add_field(name="🏥เคสสะสม (ยกเว้นเดินทางจากต่างประเทศ)", value=f"{ans[i]['total_case_excludeabroad']:,}", inline=False)
            embed.add_field(name="🪦เสียชีวิต", value=f"{ans[i]['new_death']:,}", inline=False)
            embed.add_field(name="🪦เสียชีวิตสะสม", value=f"{ans[i]['total_death']:,}", inline=False)
            embed.add_field(name="📅ข้อมูลอัปเดตล่าสุด", value=ans[i]['update_date'], inline=False)
            embed.set_footer(text="ข้อมูลจาก covid19.ddc.moph.go.th")
            #await asyncio.gather(message.author.mention, message.channel.send(embed=embed))
            await message.channel.send(embed=embed)