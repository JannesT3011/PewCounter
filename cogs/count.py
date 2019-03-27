import urllib.request
import json
import discord
from discord.ext import commands
import asyncio
from config import youtube_api_key

class PewVsTse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ytkey = youtube_api_key

    def _pewsubs(self):
        """GET THE SUBS OF PEWDIEPIE"""
        data_pew = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=pewdiepie&key={self.ytkey}").read()
        subs_pew = json.loads(data_pew)["items"][0]["statistics"]["subscriberCount"]
        return subs_pew

    def _tssubs(self):
        """GET THE SUBS OF T-SERIES"""
        data_ts = urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=tseries&key={self.ytkey}").read()
        subs_ts = json.loads(data_ts)["items"][0]["statistics"]["subscriberCount"]
        return subs_ts

    def _difference(self):
        """CALCULATE THE DIFFERENCE BETWEEN THE SUBS"""
        diff = int(self._pewsubs()) - int(self._tssubs())
        if diff < 0:
            diff = diff * -1
        return diff

    def _embed(self, ctx):
        """CREATES THE EMBED"""
        title = "**PewDiePie vs. Tseries Counter**"
        embed = discord.Embed(title=title, timestamp=ctx.message.created_at)
        embed.add_field(name="PewDiePie subs:", value=f"`{'{:,d}`'.format(int(self._pewsubs()))}")
        embed.add_field(name="Subs Difference:", value=f"`{'{:,d}`'.format(int(self._difference()))}")
        embed.add_field(name="T-Series subs:", value=f"`{'{:,d}`'.format(int(self._tssubs()))}")
        embed.set_footer(text="!~Subscribe to PewDiePie~!")
        return embed

    @commands.command(name="count", aliases=["counter", "pew"])
    async def _counter(self, ctx):
        """SUBSCRIBER COUNTER FOR PEWDIEPIE AGAINST T-SERIES"""

        msg = await ctx.send(embed=self._embed(ctx))
        while not self.bot.is_closed():
            await asyncio.sleep(5)
            await msg.edit(embed=self._embed(ctx))

def setup(bot):
    bot.add_cog(PewVsTse(bot))
