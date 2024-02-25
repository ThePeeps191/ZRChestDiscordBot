from discord import Intents, Client, Message, Game
import requests

intents = Intents.default()
intents.message_content = True
client = Client(intents = intents)

def check_userkey(userkey):
	test_r = requests.get(f"https://zombsroyale.io/api/user/{userkey}").json()
	return True if test_r["status"] == "success" else False

async def send_message(message, user_message):
	if is_private := user_message[0] == '?':
		user_message = user_message[1:]
	await message.author.send(user_message) if is_private else await message.channel.send(user_message)

@client.event
async def on_ready():
	await client.change_presence(activity=Game('!open [userkey]'))
	print(f'{client.user} is online')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	username = str(message.author)
	user_message = message.content
	channel = str(message.channel)
	s = user_message.split()
	if len(s) != 2 and s[0] == "!open":
		await send_message(message, "Please use the command `!open [account userkey]` in that format.")
	elif len(s) == 2 and s[0] == "!open":
		userkey = s[1]
		if not check_userkey(userkey):
			await send_message(message, "Please enter a valid ZR account userkey.")
		else:
			r1 = requests.post(f"https://zombsroyale.io/api/user/{userkey}/rewards/claim", data = {"type" : "gift"}).json()
			if r1["status"] == "error":
				await send_message(message, r1["message"])
			else:
				r2 = requests.post(f"https://zombsroyale.io/api/user/{userkey}/pack/open", data = {"packId" : 1}).json()
				await send_message(message, f'You got item with itemID {r2["rewards"][0]["itemId"]} from your chest.')

if __name__ == "__main__":
	client.run("token")
