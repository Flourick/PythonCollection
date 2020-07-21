import sys, logging, time
import asyncio
from mcstatus import MinecraftServer

import discord
from discord.ext import commands
from discord.ext.commands import Bot

#########################
######## FILL IN ########
#########################
TOKEN = ""
SERVER_NAME = "My Cool Server"
SERVER_ADDRESS = ""
PORT = "25565"
COMMAND_PREFIX = "/"
#########################
#########################

class ServerStatus:
	def __init__(self, current_players, max_players, players, version):
		self.current_players = current_players
		self.max_players = max_players
		self.players = players
		self.version = version

def check():
	if sys.version_info[0] < 3:
		raise Exception("You must use Python 3.4 or higher.")
	elif sys.version_info[1] <  4:
		raise Exception("You must use Python 3.4 or higher.")

def get_server_status():
	try:
		status = server.status()

		players = []
		if status.players.sample == None:
			players = ""
		else:
			for player in status.players.sample:
				players.append(player.name)

			players =  ", ".join(players)

		return ServerStatus(status.players.online, status.players.max, players, status.version.name)
	except Exception as e:
		return None

async def status_task():
	while True:
		stat = get_server_status()

		if stat == None:
			await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name="connection..."))
		elif stat.current_players > 0:
			await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=str(stat.current_players) + "/" + str(stat.max_players)))
			logging.info("playing " + str(stat.current_players) + "/" + str(stat.max_players))
		else:
			await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=str(stat.current_players) + "/" + str(stat.max_players)))
			logging.info("server empty")

		await asyncio.sleep(30)

async def remove_message(sent, ctx):
	await asyncio.sleep(60)
	await ctx.channel.delete_messages([sent])

if __name__ == "__main__":
	check()

	logging.basicConfig(
    	format="[%(asctime)s]: %(message)s",
    	level=logging.INFO,
    	datefmt='%d-%m-%Y %H:%M:%S')

	server = MinecraftServer.lookup(SERVER_ADDRESS + ":" + PORT)

	bot = commands.Bot(command_prefix=COMMAND_PREFIX)
	bot.remove_command("help")

	@bot.event
	async def on_ready():
		logging.info("BOT CONNECTED!")
		bot.loop.create_task(status_task())

	@bot.command(name="status", aliases=["server"])
	async def status(ctx):
		stat = get_server_status()

		if stat == None:
			emb = discord.Embed(
				title=SERVER_NAME + " status",
				description="Unable to get server status!",
				colour=discord.Colour.red()
			)
		else:
			emb = discord.Embed(
				title=SERVER_NAME + " status",
				description="**" + str(stat.current_players) + "/" + str(stat.max_players) + "**" + " player(s) online.\n" if stat.current_players > 0 else "*Nobody is playing!*",
				colour=discord.Colour.green() if stat.current_players > 0 else discord.Colour.orange()
			)
			emb.add_field(name="Players:", value=stat.players if stat.current_players > 0 else "*None*", inline=False)
			emb.add_field(name="Version:", value=stat.version, inline=False)
			emb.set_thumbnail(url="https://api.mcsrvstat.us/icon/" + SERVER_ADDRESS + ":" + PORT)

		sent = await ctx.send(embed=emb)
		await ctx.channel.delete_messages([ctx.message])
		asyncio.create_task(remove_message(sent, ctx))

	bot.run(TOKEN, reconnect=True)