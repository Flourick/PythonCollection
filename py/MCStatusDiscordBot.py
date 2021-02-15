import sys, logging
import asyncio
from mcstatus import MinecraftServer

import discord
from discord.ext import commands

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

def version_check():
	if sys.version_info < (3, 5):
		raise Exception("You must use Python 3.5 or higher.")

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
	await bot.wait_until_ready()

	while not bot.is_closed():
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
	version_check()

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

		task_found = False
		for task in asyncio.all_tasks():
			if task.__str__().__contains__("status_task()"):
				task_found = True

		if not task_found:
			bot.loop.create_task(status_task())

	@bot.event
	async def on_resumed():
		logging.info("BOT CONNECTION RESUMED!")
		
		task_found = False
		for task in asyncio.all_tasks():
			if task.__str__().__contains__("status_task()"):
				task_found = True

		if not task_found:
			bot.loop.create_task(status_task())

	# @bot.event
	# async def on_member_join(member):
	# 	# Automatically puts user in a role after he joins, uncomment to enable and fill in a role name
	# 	await member.add_roles(discord.utils.get(member.guild.roles, name="CHANGE ME TO A ROLE NAME"))

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
