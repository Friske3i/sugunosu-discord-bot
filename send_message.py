import discord
import datetime
import os
import asyncio

# GitHubの「Secrets」からトークンなどを読み込む設定
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# 日本時間のタイムゾーン
JST = datetime.timezone(datetime.timedelta(hours=9))
REACTIONS = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:']

def get_next_week_dates():
    today = datetime.datetime.now(JST).date()
    days_until_monday = (0 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = today + datetime.timedelta(days=days_until_monday)
    return [(next_monday + datetime.timedelta(days=i)).strftime('%m/%d') for i in range(7)]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            dates = get_next_week_dates()
            content = f"@everyone 来週のスケジュールチェックです\n\n"
            content += f"{dates[0]} (月) :one:\n{dates[1]} (火) :two:\n{dates[2]} (水) :three:\n"
            content += f"{dates[3]} (木) :four:\n{dates[4]} (金) :five:\n{dates[5]} (土) :six:\n"
            content += f"{dates[6]} (日) :seven:"

            msg = await channel.send(content)
            for r in REACTIONS:
                await msg.add_reaction(r)
            print("送信完了")
        
        await self.close() # 送信が終わったら終了する

# 実行
intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)