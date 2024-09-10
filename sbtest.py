from datetime import datetime, timedelta
import discord
from discord.ext import commands
import requests
import json
import asyncio 
from bs4 import BeautifulSoup
import aiohttp
import json
import os
from pathlib import Path
import requests
from datetime import datetime, timedelta
import pyfiglet
import urllib.parse

folder_sb = os.path.dirname(os.path.realpath(__file__))

json_file = os.path.join(folder_sb, 'config.json')

if os.path.exists(json_file):

    with open(json_file, 'r') as file:
        sb = json.load(file)
else:
    sb = {}

TOKEN = sb.get("TOKEN", "").strip()

if not TOKEN:
    TOKEN = input("Enter your token >.< ")
    sb["TOKEN"] = TOKEN


    with open(json_file, "w") as file:
        json.dump(sb, file, indent=4)

bot = commands.Bot(command_prefix='`', self_bot=True,)

@bot.command()
async def spam(ctx, Number=None, *, message):
  await ctx.message.delete()
  count = 0
  while count < int(Number):
      await ctx.send("{}".format(message))
      count = count + 1

@bot.command()
async def meow(ctx):
    await ctx.message.delete()
    await ctx.send('''```
       ,
       \\`-._           __
        \\\\  `-..____,.'  `.
         :`.         /    \\`.
         :  )       :      : \\
          ;'        '   ;  |  :
          )..      .. .:.`.;  :
         /::...  .:::...   ` ;
         ; _ '    __        /:\\
         `:o>   /\\o_>      ;:. `.
        `-`.__ ;   __..--- /:.   \\
        === \\_/   ;=====_.':.     ;
         ,/'`--'...`--....        ;
              ;                    ;
            .'                      ;
          .'                        ;
        .'     ..     ,      .       ;
       :       ::..  /      ;::.     |
      /      `.;::.  |       ;:..    ;
     :         |:.   :       ;:.    ;
     :         ::     ;:..   |.    ;
      :       :;      :::....|     |
      /\\     ,/ \\      ;:::::;     ;
    .:. \\:..|    :     ; '.--|     ;
   ::.  :''  `-.,,;     ;'   ;     ;
.-'. _.'\\      / `;      \\,__:      \\
`---'    `----'   ;      /    \\,.,,,/
                   `----`              meow
```''')

@bot.command()
async def deletechannels(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        await channel.delete()
    return

@bot.command()
async def commands(ctx):
    await ctx.message.delete()
    await ctx.send('''```
- skibidi toilet -

meow - sends an ASCII art of a cat
lookup - looks up an IP address
spam - sends a message as many times as you choose (input how many times, then the message)
ban - bans a user with an optional reason
kick - kicks a user from the server
unban - unbans a user
purge - deletes a specified number of messages
search - searches Google for a query (currently outdated)
deletechannels - deletes all channels in the server
createchannels - creates a specified number of text channels with a given name
massban - bans all members in the server with a reason
webhookmessage - sends a message via webhook with a specified username
webhookspam - spams a message a specified number of times using webhooks
nuke - deletes all channels, creates new channels, deletes all roles, creates new roles, and bans all members
```''')

@bot.command()
async def lookup(ctx, TARGET_IP=None):
    if TARGET_IP:
        try:
            RESPONSE = requests.get('http://ip-api.com/json/{}'.format(TARGET_IP))
            CONTENT = json.loads(RESPONSE.text)

            if str(CONTENT['status']) == 'success':
                await ctx.message.delete()
                one = TARGET_IP
                two = CONTENT['isp']
                three = CONTENT['city']
                four = CONTENT['regionName']
                five = CONTENT['lat']
                six = CONTENT['lon']

                await ctx.send('''```py
IP: {} 
ISP: {}
City: {}
Region: {}
Coordinates: {} LON, {} LAT
```'''.format(one, two, three, four, five, six))
            else:
                if str(CONTENT['message']) == 'invalid query':
                  await ctx.message.delete()
                  await ctx.send('``INVALID IP``')
        except:
            await ctx.send('`An error has occurred.`')
        return

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned/kicked for {reason}")
    await ctx.message.delete()
    return

@bot.command()
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.message.delete()
    return

@bot.command()
async def unban(ctx, member: discord.Member,):
    await member.unban()
    await ctx.message.delete()
    return

@bot.command()
async def purge(ctx, amount:int=None):
    try:
        if amount is None:
            await ctx.send("Invalid amount")
        else:
            deleted = await ctx.channel.purge(limit=amount, before=ctx.message, check=message.author == bot.user) //message.author == bot.user
            asd = await ctx.send('Deleted {} message(s)'.format(len(deleted)))
            await asyncio.sleep(3)
            await asd.delete()
    except:
        try:
            await asyncio.sleep(1)
            c = 0
            async for message in ctx.message.channel.history(limit=amount):
                if message.author == bot.user:
                    c += 1
                    await message.delete()
                else:
                    pass
            asd = await ctx.send('Deleted {} message(s)'.format((c)))
            await asyncio.sleep(3)
            await asd.delete()
        except Exception as e:
            await ctx.send(f"Error: {e}")
        return

@bot.command()
async def createchannels(ctx, number: int, channel_name):
    guild = ctx.guild
    channel_amount = 0
    while channel_amount < number:
       await guild.create_text_channel(channel_name)
       channel_amount +=1
    
@bot.command()
async def massban(ctx,  reason):
    guild= ctx.guild
    if guild is None:
        
        return
    
    if not ctx.author.guild_permissions.ban_members:
        
        return
    
    for member in guild.members:
        if member != bot.user:
            try:
                await ctx.guild.ban(member, reason=reason)
            except discord.Forbidden:
                print("no workie need perms")
            except discord.HTTPException:
                print("also no workie")

@bot.command()
async def webhookmessage(ctx, message, user_name: str):
    channel = ctx.channel
    if channel is not None:
        webhook = await channel.create_webhook(name="webspam")
        await webhook.send(message, username=user_name)
    else:
        pass

@bot.command()
async def webhookspam(ctx, amount: int, message: str):
    channel = ctx.channel
    counter = 0
    webhooks = []
    webhook_limit = 15  

    if channel is not None:
        existing_webhooks = await channel.webhooks()
        for webhook in existing_webhooks:
            try:
                await webhook.delete()
            except discord.Forbidden:
                print("noooo")
            except discord.HTTPException:
                print(f"error: {e}")
        
        for i in range(webhook_limit):
            webhook = await channel.create_webhook(name=f"webspam-{i + 1}")
            webhooks.append(webhook)
        
        try:
            while counter < amount:

                for webhook in webhooks:
                    if counter >= amount:
                        break  

                    try:
                        await webhook.send(message, username="Lawcan")
                        counter += 1
                        
                        await asyncio.sleep(1)  
                    except discord.HTTPException as e:
                        if e.status == 429:  
                            
                            new_webhook = await channel.create_webhook(name=f"webspam-{len(webhooks) + 1}")
                            webhooks.append(new_webhook)
                        else:
                            raise 

        except discord.Forbidden:
            await ctx.send("need admin")
        except discord.HTTPException as e:
            await ctx.send(f"An HTTP error occurred: {e}")
#needs work

@bot.command()
async def nuke(ctx):
    #Permission management
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("You don't have perms silly :3.")
        return

    guild = ctx.guild

    #mas channel delete
    for channel in guild.channels:
        try:
            await channel.delete()
        except discord.Forbidden:
            await ctx.send(f"Cannot delete channel: {channel.name}. lf perms.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to delete channel: {channel.name} due to an HTTP error >.<. {e}")

    #Channel spam
    channel_amount = 0
    number = 50
    while channel_amount < number:
        try:
            await guild.create_text_channel("Lawcan")
            channel_amount += 1
        except discord.Forbidden:
            await ctx.send("lf perms")
            break
        except discord.HTTPException as e:
            await ctx.send(f"Failed to create channel due to an HTTP error >.<. error is {e}")
            break

    #massban
    for member in guild.members:
        if member != bot.user:
            try:
                await guild.ban(member, reason="Lawcan")
            except discord.Forbidden:
                await ctx.send(f"Failed to ban {member}. lf perms.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to ban {member} due to an HTTP error. {e}")

    #mass role delete
    roles = ctx.guild.roles
    roles_to_delete = [role for role in roles if role.name != "@everyone" and role != ctx.guild.me.top_role]

    for role in roles_to_delete:
        try:
            await role.delete
        except discord.Forbidden:
            await ctx.send("lf perms")
            return
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error occurred while deleting role {role.name}: {e}")
            return

    #mass role create
    role_limit = 250
    role_amount = 0
    while role_amount < role_limit:
        try:
            await ctx.guild.create_role(name="Lawcan")
            role_amount += 1
        except discord.Forbidden:
            await ctx.send("lf perms")
            break
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error occurred while creating role: {e}")
            break

@bot.command()
async def spamroles(ctx, number: int, role_name: str):
    role_amount = 0
    while role_amount < number:
        try:
            # Create the role with the specified name
            await ctx.guild.create_role(name=role_name)
            role_amount += 1
        except discord.Forbidden:
            await ctx.send("Cannot create role. Missing permission.")
            break
        except discord.HTTPException as e:
            await ctx.send(f"http error {e}")
            break

async def deleteroles(ctx):

    roles = ctx.guild.roles


    roles_to_delete = [role for role in roles if role.name != "@everyone" and role != ctx.guild.me.top_role]


    for role in roles_to_delete:
        try:
            await role.delete()
        except discord.Forbidden:
            await ctx.send("Cannot delete roles. Missing permission.")
            return
        except discord.HTTPException as e:
            await ctx.send(f"HTTP error occurred while deleting role {role.name}: {e}")
            return



@bot.command()
async def search(ctx, *, query: str):
    await ctx.message.delete()
    search_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    
    search_results = []
    for g in soup.find_all('div', class_='tF2Cxc', limit=6):  
        title = g.find('h3').text
        link = g.find('a')['href']
        search_results.append(f"[{title}]({link})")

    if search_results:
        await ctx.send("\n".join(search_results))
    else:
        await ctx.send("No results found.")

@bot.command()
async def ascii(ctx, *, message):
    await ctx.message.delete()
    ascii_art = pyfiglet.figlet_format(message)
    await ctx.send(f"```{ascii_art}```")

API_KEY = 'a63ac83a451949e1ae91fe3bbf2ee450'#replace with your own api key if you want >.<
BASE_URL = 'https://www.bungie.net/Platform/Destiny2/'

headers = {
    'X-API-Key': API_KEY
}

raid_name_map = {
    2693136600: 'Leviathan',
    3089205900: 'Eater_of_Worlds',
    119944200: 'Spire_of_Stars',
    548750096: 'Scourge_of_the_Past',
    3333172150: 'Crown_of_Sorrow',
    2122313384: 'Last_Wish',
    1042180643: 'Garden_of_Salvation',
    910380154: 'Deep_Stone_Crypt',
    3881495763: 'Vault_of_Glass',
    1441982566: 'Vow_of_the_Disciple',
    1374392663: 'Kings_Fall',
    2381413764: 'Root_of_Nightmares',
    2192826039: 'Salvation\'s Edge'
}
#chatgpt api requests bungie api docs are impossible to read
def get_membership_id_and_type(username):
    
    encoded_username = urllib.parse.quote(username)
    search_endpoint = f'{BASE_URL}SearchDestinyPlayer/-1/{encoded_username}/'
    
    try:
        response = requests.get(search_endpoint, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return None, None, f"Error fetching membership details: {str(e)}"
    
    data = response.json()
    if 'Response' in data and data['Response']:
        membership_type = data['Response'][0]['membershipType']
        membership_id = data['Response'][0]['membershipId']
        return membership_id, membership_type, None
    else:
        return None, None, "Username not found or invalid."

def get_most_recent_raid(membership_id, membership_type):
    characters_endpoint = f'{BASE_URL}{membership_type}/Profile/{membership_id}/?components=200'
    try:
        response = requests.get(characters_endpoint, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching character data: {str(e)}"

    characters_data = response.json()
    character_ids = characters_data['Response']['characters']['data'].keys()

    most_recent_raid = None
    most_recent_raid_index = None

    for character_id in character_ids:
        activities_endpoint = f'{BASE_URL}{membership_type}/Account/{membership_id}/Character/{character_id}/Stats/Activities/'
        params = {
            'mode': '4',
            'count': '1',
            'page': '0'
        }

        try:
            response = requests.get(activities_endpoint, headers=headers, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Error fetching activities data for character {character_id}: {str(e)}"

        data = response.json()
        activities = data['Response']['activities']
        if activities:
            last_raid = activities[0]
            raid_time = datetime.fromisoformat(last_raid['period'].replace('Z', '+00:00'))
            duration_seconds = last_raid['values']['activityDurationSeconds']['basic']['value']
            duration = timedelta(seconds=duration_seconds)
            raid_index = activities.index(last_raid) + 1  

            if most_recent_raid is None or raid_time > most_recent_raid['time']:
                most_recent_raid = {
                    'time': raid_time,
                    'raid': last_raid,
                    'duration': duration
                }
                most_recent_raid_index = raid_index

    if most_recent_raid:
        raid_reference_id = most_recent_raid['raid']['activityDetails']['referenceId']
        raid_name = raid_name_map.get(raid_reference_id, "Unknown Raid")
        duration = most_recent_raid['duration']

        return (
            f"Most recent raid completion:\n"
            f"Raid Name: {raid_name}\n"
            f"Completion Time: {most_recent_raid['time']}\n"
            f"Duration: {str(duration)}\n"
            f"Raid Index: {most_recent_raid_index}"
        )
    else:
        return "No raid completions found for any character."

@bot.command()
async def lastraid(ctx, username: str = None):
    if username is None:
        username = "lawcan#7065"  
    membership_id, membership_type, error = get_membership_id_and_type(username)
    if error:
        await ctx.send(error)
        return

    await ctx.message.delete()
    raid_info = get_most_recent_raid(membership_id, membership_type)
    await ctx.send(f"lawcan\n{raid_info}\n{username}")

bot.run(TOKEN)