import requests
import discord
from events.base_event      import BaseEvent


class ChangePresence(BaseEvent):

    def __init__(self):
        interval_minutes = 360  
        super().__init__(interval_minutes)

    async def run(self, client):
        r = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
        ans = r.json()
        nc = ans[0]['total_case']
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{nc:,} new Covid cases'))
