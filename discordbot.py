from discord.ext import commands
import os
import traceback
import urllib.request
import json

bot = commands.Bot(command_prefix='!')
token = os.environ['DISCORD_BOT_TOKEN']
citycode = '130010'
CHANNEL_ID = 706616249383256084

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
    
@bot.command()
async def server(ctx):
    await ctx.send(getserver())
    
@tasks.loop(seconds=60)
async def loop():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(getserver())  

def getserver():
        resp = urllib.request.urlopen('http://nyatla.jp/ws/mcsapi/mcsapi.php?cmd=si&s=106.72.172.97&p=6016&f=json').read().decode('utf-8','replace')
    
    resp = resp.replace('online', '"online"')
    resp = resp.replace('server', '"server"')
    resp = resp.replace('name', '"name"')
    resp = resp.replace('port', '"port"')
    resp = resp.replace('result', '"result"')
    resp = resp.replace('retcode', '"retcode"')
    resp = resp.replace('title', '"title"')
    resp = resp.replace('user', '"user"')
    resp = resp.replace('active', '"active"')
    resp = resp.replace('max', '"max"')
    resp = resp.replace('update_time', '"update_time"')
    
    resp = json.loads(resp, strict=False)
    msg = "```"
    msg += "Server:" + resp['server']['name'] + ":" + str(resp['server']['port']) + "\n"
    msg += "Online:" + str(resp['online']) + "\n"
    msg += "Active:" + str(resp['result']['user']['active'])
    msg += "```"
    return msg
    
#ループ処理実行
loop.start()

bot.run(token)
