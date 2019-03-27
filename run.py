from discord.ext import commands
import discord
import asyncio
from config import prefix, description, token

COGS = ["cogs.count"]
TOKEN = token
PREFIX = prefix
DESCRIPTION = description

async def run():
    """RUN THE BOT"""
    bot = Bampy(description=DESCRIPTION)

    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        await bot.logout()
        print(f"Connection closed!")


class Bampy(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=PREFIX,
            description=kwargs.pop("description")
        )

        for ext in COGS:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f"Cant load {ext}")
                raise e

    async def on_ready(self):
        print("##########\n"f"{self.user.name}\n"f"{self.user.id}\n""##########")
        print(discord.utils.oauth_url(self.user.id))

    async def on_message(self, message):
        if not message.guild:
            return

        await self.process_commands(message)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
