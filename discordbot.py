from discord.ext import commands
import discord
import os
import traceback
from schedule import show_schedule

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

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
    channel = await client.get_channel(365144324364828677)
    message = await channel.fetch_message(801838502387646546)
    await message.edit(content="newcontent")


bot.run(token)
