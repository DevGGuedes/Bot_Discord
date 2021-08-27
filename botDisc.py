import re
from traceback import print_exception, print_tb
import discord
from discord.errors import PrivilegedIntentsRequired
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtube_dl
import asyncio

load_dotenv()
# Get the API token from the .env file.
#DISCORD_TOKEN = os.getenv("discord_token")


intents = discord.Intents().all()
#intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)
songs = asyncio.Queue()
play_next_song = asyncio.Event()

FILA_MUSICAS = []
#music_on = False

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class Robot():
    #music_on = None
    def __init__(self, music = False, list_musics = []):
        #super(robot, self).__init__()
        self.music = music
        self.list_musics = list_musics
        self.voice_connect = False
        self.voice_client = None

    #Getter Music
    @property
    def music(self):
        return self._music

    @property
    def list_musics(self):
        return self._list_musics

    @property
    def voice_connect(self):
        return self._voice_connect
    
    @property
    def voice_client(self):
        return self._voice_client

    @music.setter
    def music(self, val):
        self._music = val
    
    @list_musics.setter
    def list_musics(self, val):
        self._list_musics = val

    @voice_connect.setter
    def voice_connect(self, val):
        self._voice_connect = val

    @voice_client.setter
    def voice_client(self, val):
        self._voice_client = val

    @bot.command(name='qt', help='To play song')
    async def add_music(self, ctx, url):
        print(len(self.queue))
        print(self.queue)

robot = Robot()

@bot.command(name='f', help='Fila')
async def get_fila(ctx):
    current = await songs.get()
    print(f'current {current}')

@bot.command(name='q', help='Colocar na fila')
async def get_fila(ctx, url):
    #if not bot.is_voice_connected(ctx.message.server):
    channel = ctx.message.author.voice.channel
    #if ctx.message.author.voice.channel.connect:
    #voice = await channel.connect()
        #print('')
    #else:
        #print('')
        #voice = await channel.connect()

    #filename = await YTDLSource.from_url(url, loop=bot.loop)
    #player = voice.play(discord.FFmpegPCMAudio(executable=r"C:\FFmpeg\bin\ffmpeg.exe", source=filename))
    #asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))
    #player = await voice.create_ytdl_player(url)
    await songs.put(url)
    print(songs)
    items = []
    item = await songs.get()
    print(f'item {item}')
    #print(asyncio.Queue)
    current = await songs.get()
    #print(f'current {current}')

global list_musics
list_musics = []

@bot.command(name='add', help='To play song')
async def add_music(ctx, url):
    robot.list_musics.append(url)
    embed = discord.Embed(
        title = "Adicionado na Fila",
        color = discord.Color.blue()
    )
    
    embed.add_field(name="Quantidade de musicas:", value=len(robot.list_musics), inline=False)
    embed.add_field(name="Musica:", value=url, inline=False)
    await ctx.send(embed=embed)
    print(len(list_musics))


@bot.command(name='list', help='To play song')
async def send_list(ctx):
    if len(robot.list_musics) > 0:
        nomeMusica = ""
        for i in list_musics:
            index = list_musics.index(i)

        embed = discord.Embed(
            title = "Musicas",
            color = discord.Color.blue()
        )
        
        embed.add_field(name="Quantidade de musicas:", value=len(robot.list_musics), inline=False)
        embed.add_field(name="Musica:", value="None", inline=False)
        await ctx.send(embed=embed)
        
    else:
        await ctx.send("Nenhuma musica está na fila.")

global music 
music = None

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    
    robot.voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    #print(f'voice_client {robot.voice_client}')
    if robot.voice_client == None:
        await join(ctx)

    #print(f'voice_client {robot.voice_client}')
    #print(f'robot.voice_connect {robot.voice_connect}')
    if robot.voice_client != None and robot.voice_connect != True:
        #print(voice_client.is_connected())
        robot.voice_connect = True
        #print(robot.voice_connect)
        #voice_client = True
        #print(voice_client)
        await ctx.send(f"**Bot Conectado em** {ctx.message.author.voice.channel}")
    
    robot.list_musics.append(url)
    print(len(robot.list_musics))

    #for i in robot.list_musics:
    #    print(i)

    #print(f'robot.music {robot.music}')
    #print(f'robot._music - {robot._music}')
    #robot = Robot()
    #print(f'robot.music 1- {robot.music}')
    #if robot.music != True:
        #await join(ctx)
        #robot = Robot(True, url)
        #robot.music = True
        #print(f'robot.music {robot.music}')
        #print(f'Classe Ativa')
        #print(f'robot.music {robot.music}')
        #print(f'robot._music {robot._music}')
    #elif Robot.music == True:
        #print('Ja Ativo')
        
    
    #print(f'active - {active}')
    #if not ctx.message.author.name=="Rohan Krishna" :
    #     await ctx.send('NOT AUTHORISED!')
    #     return

    try :
        #list_musics.append(url)

        for i in robot.list_musics:

            server = ctx.message.guild
            voice_channel = server.voice_client
            print(voice_channel.is_playing)
            
            #desc = ctx.guild.description
            #icon = str(ctx.guild.icon_url)

            async with ctx.typing():
                #filename = await YTDLSource.from_url(url, loop=bot.loop)
                filename = await YTDLSource.from_url(i, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable=r"C:\FFmpeg\bin\ffmpeg.exe", source=filename))
                print(voice_channel.is_playing)

            embed = discord.Embed(
                title = "Musica",
                description = "teste desc",
                color = discord.Color.blue()
            )
            
            embed.add_field(name="Adicionado Por:", value=ctx.message.author.mention, inline=False)
            embed.add_field(name="Tocando:", value=i, inline=False)
            if len(robot.list_musics) > 1:
                embed.add_field(name="Na fila:", value=len(robot.list_musics), inline=False)

            music = True
            #print(f'music - {music}')

            await ctx.send(embed=embed)
        #await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("Não foi possivel reproduzir a musica.")

#robot = Robot()

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    #voice_client = ctx.bot.voice_clients
    #print(voice_client)
    #print(ctx.bot.voice_clients)
    #await is_connected(ctx)
    
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        active = False
        return
    
    #if not voice_client:
    #    channel = ctx.message.author.voice.channel
    #    await channel.connect()
    if ctx.message.author.voice.channel.connect:
        channel = ctx.message.author.voice.channel
        #print(f'ctx.message.author.voice.channel - {ctx.message.author.voice.channel}')
        robot.voice_connect = True
        await channel.connect()
        robot.voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return
    else:
        channel = ctx.message.author.voice.channel
        #print(f'ctx.message.author.voice.channel = {ctx.message.author.voice.channel}')
        active = True
        await channel.connect()
    return active
    #channel = ctx.message.author.voice.channel
    #await channel.connect()
    return

#robot = Robot()

@bot.command(name='connected', help='Connected')
async def is_connected(ctx):
    
    #print(f'robot.voice_connect {robot.voice_connect}')

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    #print(voice_client)
    #print(voice_client.is_connected())
    #connected = voice_client.is_connected()

    #if robot.voice_connect == False:
    #if voice_client == None:
        #await ctx.send(f"**Sem conexao com um canal de voz**")
    if voice_client != None and robot.voice_connect != True:
        #print(voice_client.is_connected())
        robot.voice_connect = True
        print(robot.voice_connect)
        #voice_client = True
        #print(voice_client)
        await ctx.send(f"**Bot Conectado em** {ctx.message.author.voice.channel}")
    else:
        await ctx.send(f"**Bot Ja Conectado em** {ctx.message.author.voice.channel}")

    #return voice_client and voice_client.is_connected()
    

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
        await ctx.send("**Musica pausada**.")
    else:
        #await ctx.send("The bot is not playing anything at the moment.")
        await ctx.send("O bot não está tocando nada no momento")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
        await ctx.send("**Continuar Musica**.")
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
    

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    robot.list_musics = []
    voice_client = ctx.message.guild.voice_client

    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        active = False
        return

    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.event
async def on_ready():
    print('Running!')
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File('giphy.png'))
        print('Active in {}\nMember Count : {}'.format(guild.name,guild.member_count))

@bot.command(name = "hello", help = "Prints details of Author")
async def whats_my_name(ctx) :
    #await ctx.send('Hello {}'.format(ctx.author.name)) Oi Luvi, casada? rs
    await ctx.send(f'Oi {ctx.message.author.mention}, Casado(a)? rs')
    #await ctx.send(f"Teste {ctx.message.author.mention}")
    #embed = discord.Embed(description='\n1')
    #await bot.say(embed=embed)

@bot.command(name = "members", help = "Prints details of Server")
async def where_am_i(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if str(channel) == "general" or str(channel) == "geral":
            on_mobile=False
            if member.is_on_mobile() == True :
                on_mobile = True
            
            #await channel.send("Welcome to the Server {}!!\n On Mobile : {}".format(member.name,on_mobile))     
            await channel.send(f'Bem-Vindo {member.name}. Respeite e seja Humilde')             
        
# TODO : Filter out swear words from messages

@bot.command()
async def tell_me_about_yourself(ctx):
    text = "My name is WallE!\n I was built by Kakarot2000. At present I have limited features(find out more by typing !help)\n :)"
    await ctx.send(text)

@bot.event
async def on_message(message) :
    # bot.process_commands(msg) is a couroutine that must be called here since we are overriding the on_message event
    await bot.process_commands(message) 
    if str(message.content).lower() == "hello":
        await message.channel.send('Hi!')
    
    if str(message.content).lower() in ['swear_word1','swear_word2']:
        await message.channel.purge(limit=1)


if __name__ == "__main__" :
    #bot.run(DISCORD_TOKEN)
    
    bot.run('ODc5NTEwMzYxMjU3MTc3MDk5.YSQx2g.MKimKZyLuvzDBE60xzWvtJeoTec')