import discord
from discord.ext import commands

# Set bot command prefix (e.g., !hello)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

TOKEN = "Token goes here"
bot.run(TOKEN)

!pip install nest_asyncio
import nest_asyncio  # Import nest_asyncio

# Set bot command prefix (e.g., !hello)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
bot.run(TOKEN)



# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
bot.run(TOKEN)

#responding to specic words
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevent bot from replying to itself

    if "hello" in message.content.lower():
        await message.channel.send(f"Hey {message.author.mention}!")

    await bot.process_commands(message)  # Ensures commands still work
#playing music
import youtube_dl
import discord
from discord.ext import commands

@bot.command()
async def join(ctx):
    """Bot joins the voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel!")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command()
async def play(ctx, url):
    """Bot plays music from a YouTube URL."""
    if not ctx.voice_client:
        await ctx.invoke(join)

    ydl_opts = {"format": "bestaudio"}
    ffmpeg_opts = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["url"]
        source = discord.FFmpegPCMAudio(url2, **ffmpeg_opts)
        ctx.voice_client.play(source)

    await ctx.send(f"Now playing: {info['title']}")
#moderation tools
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    """Kick a user from the server."""
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} was kicked. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    """Ban a user from the server."""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} was banned. Reason: {reason}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    """Mute a user by removing their ability to send messages."""
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been muted.")
#logging message
@bot.event
async def on_message_delete(message):
    channel = discord.utils.get(message.guild.text_channels, name="logs")
    if not channel:
        return  # Skip if there's no "logs" channel

    await channel.send(f"🗑️ {message.author} deleted: {message.content}")

@bot.event
async def on_message_edit(before, after):
    channel = discord.utils.get(before.guild.text_channels, name="logs")
    if not channel:
        return

    await channel.send(f"✏️ {before.author} edited a message: '{before.content}' → '{after.content}'")
