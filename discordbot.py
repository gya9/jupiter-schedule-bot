from discord.ext import commands
import discord
import os
import asyncio
import traceback
from schedule import show_schedule

bot = commands.Bot(command_prefix='/')
# token = os.environ['DISCORD_BOT_TOKEN']
token = 'ODAxODI5NzI0MTk1MjU4NDI5.YAmYHw.LLO5fQ029UQBbMwTTnuhW6vMy1M'
client = discord.Client()

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def schedule(ctx):
    msg = show_schedule()
    await ctx.send(msg)

@bot.command()
async def testing(ctx):
    channel = bot.get_channel(477180851994624000)
    message = await channel.fetch_message(801855318970859572)
    pushmsg = show_schedule()
    await message.edit(content=pushmsg)


bot.run(token)