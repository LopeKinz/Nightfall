import os
import discord, json, aiohttp, random, discord.ext
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

with open('bad_word.txt') as file:
    file = file.read().split()
#make a discord moderation bot
intents = discord.Intents.all()
bot = commands.Bot(prefix="lol.", Intents=intents,help_command=None)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)

@bot.command()
@has_permissions(administrator=True)
async def addword(ctx, word):
    with open("bad_word.txt", "a") as f:
        f.write(f'{word}\n')
        await ctx.send(f'{word} has been added to the bad word list!')

@bot.command()
@has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned!')

@bot.command()
@has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked!')
    
@bot.command()
@has_permissions(administrator=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    
@bot.command()
@has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    await member.add_roles(discord.utils.get(ctx.guild.roles, name='Muted'))
    await ctx.send(f'{member} has been muted!')
    
@bot.command()
@has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Muted'))
    await ctx.send(f'{member} has been unmuted!')
    
@bot.command()
@has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'{member} has been warned!')
    with open("warns.json", "r") as f:
        warns = json.load(f)
    if member.id in warns:
        warns[member.id] += 1
        json.dump(warns, f)
        await ctx.send(f'{member} has been warned!')
        
@bot.command()
@has_permissions(administrator=True)
async def get_warns(ctx, member: discord.Member):
    with open("warns.json", "r") as f:
        warns = json.load(f)
    if member.id in warns:
        await ctx.send(f'{member} has {warns[member.id]} warnings!')
    if warns[member.id] == 0:
        await ctx.send(f'{member} has 0 warnings!')
        
@bot.command()
@has_permissions(administrator=True)
async def clear_warns(ctx, member: discord.Member):
    with open("warns.json", "r") as f:
        warns = json.load(f)
    if member.id in warns:
        warns[member.id] = 0
        json.dump(warns, f)
        await ctx.send(f'{member} warns has been cleared!')

@bot.command()
@has_permissions(administrator=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('Channel locked!')
        
@bot.command()
@has_permissions(administrator=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('Channel unlocked!')

@bot.command()
async def help(ctx):
    await ctx.send('$addword <word> - Adds a word to the bad word list\n$ban <member> - Bans a member\n$kick <member> - Kicks a member\n$purge <amount> - Purges a certain amount of messages\n$mute <member> - Mutes a member\n$unmute <member> - Unmutes a member\n$warn <member> - Warns a member\n$get_warns <member> - Gets the amount of warns a member has\n$clear_warns <member> - Clears the warns of a member\n$lock - Locks the channel\n$unlock - Unlocks the channel\n$help - Shows this message')
    
@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.send(f'Pong! {ping}ms')

bot.run("MTAwNjk5ODE0MjUzNDgxMTY2OQ.Gc8JvP.TXDkPFowjZpOUa0Zr5b-sVMe7uuHkD9Z1OGCqU")