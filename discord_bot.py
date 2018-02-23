import discord
from discord.ext import commands
import aiohttp

from bot_config import BOT_TOKEN
bot = commands.Bot(command_prefix="!")

async def api_call(path, method="GET", **kwargs):
    """ returns discord api call """
    defaults = {
        "headers": {
            "Authorization": f"Bot {BOT_TOKEN}",
            "User-Agent": "dBot"
            }
        }
    kwargs = dict(defaults, **kwargs)
    with aiohttp.ClientSession() as session:
        print(path)
        async with session.request(method, path, **kwargs) as response:
            assert 200 == response.status, response.reason
            return await response.json()


@bot.event
async def on_ready():
    print('Logged in')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

@bot.command(pass_context=True)
async def vod_status(ctx):
    await api_call(path='/vod_status', data=dict(username=str(ctx.message.author)))

bot.run(BOT_TOKEN)


