import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix='!')
songs = asyncio.Queue()
play_next_song = asyncio.Event()


@client.event
async def on_ready():
    print('client ready')


async def audio_player_task():
	while True:
		play_next_song.clear()
		current = await songs.get()
		print(current)
		current.start()
		await play_next_song.wait()
        

@client.command(name='list',pass_context=True)
async def list(ctx):
	print(songs)
	#print(len(songs))


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)


@client.command(name='play',pass_context=True)
async def play(ctx, url):

	channel = ctx.message.author.voice.channel

	if ctx.message.author.voice.channel.connect:
		voice = await channel.connect()
	else:
		print('')

	#voice = await client.join_voice_channel(channel)

	#if not client.is_voice_connected(ctx.message.server):
	#if not ctx.message.author.voice.channel.connect:
	#voice = await channel.connect(ctx.message.author.voice_channel)
	#voice = await channel.connect(ctx.message.author.voice.channel)
	#voice_channel = ctx.message.author.voice.channel
	voice_channel = ctx.message.author.voice.channel.id
	#print(f'voice_channel {voice_channel}')
	#voice = await client.join_voice_channel(voice_channel)
	
	#else:
	#	voice = client.voice_client_in(ctx.message.server)
	
	YDL_OPTIONS = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.%(ext)s',
    }

	#with YoutubeDL(YDL_OPTIONS) as ydl:
	#	ydl.download(url, download=True)

	voice.play(FFmpegPCMAudio("SO_TAPAO_NERVOSO_VS_CATUCADA_VIOLENTA_-_MC_Gui_Andrade_MC_Fahah_e_MC_Livinho_DJ_DN-_oJpMmHx8wY.webm", executable=r"C:\FFmpeg\bin\ffmpeg.exe"))
	player = voice.is_playing()


	#player = await voice.create_ytdl_player(url, after=toggle_next)
	#player = voice.create_ffmpeg_player('Tapao_Nervoso-v1b4ULqG_mk.webm', after=lambda: print('done'))
	#player = voice.create_ffmpeg_player(url, after=lambda: print('done'))

	#player = await voice.create_ytdl_player(url, after=toggle_next)
    #await songs.put(player)

	await songs.put(player)

client.loop.create_task(audio_player_task())

client.run('ODc5NTEwMzYxMjU3MTc3MDk5.YSQx2g.SNBnttk3zFNrrRMRrBzesmbutOU')