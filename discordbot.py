from discord.ext import commands
import os
import traceback
import urllib.request
import json

bot = commands.Bot(command_prefix='!')
token = os.environ['DISCORD_BOT_TOKEN']
citycode = '130010'

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def tenki(ctx):
    resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    resp = json.loads(resp.decode('utf-8'))
    msg = resp['location']['city'] + "の天気は\n"
    for f in resp['forecasts']:
        msg += f['dateLabel'] + "が" + f['telop'] + "\n"
    msg += "```"
    msg += resp['description']['text']
    msg += "```"
    await ctx.send(msg)
    
bot.run(token)
