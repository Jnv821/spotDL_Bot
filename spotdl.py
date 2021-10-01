import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

from credentials import discord_token, guild_ids


client = discord.Client(intents=discord.Intents.all())
# discord.Bot()
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

@client.event
async def on_ready():
    print("Ready!")

@slash.slash(name="ping",
             description="Play a round of ping-pong",
             guild_ids=guild_ids)
async def _ping(ctx): 
    await ctx.send(f"Pong! ({client.latency*1000:.1f}ms)", hidden=True)

@slash.slash(name="zsh",
             description="Instructions for users with Zsh terminals",
             guild_ids=guild_ids)
async def _zsh(ctx):
    await ctx.send('If you use Zsh terminal, **put the URL in quotes**, e.g.\n`spotdl "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b?si=TNiemvONQviXQpWPSiR2Gw"`')

@slash.slash(name="update",
             description="Various update instructions",
             guild_ids=guild_ids,
             options=[
                create_option(
                    name="location",
                    description="Where should the update come from?",
                    option_type=3,
                    required=True,
                    choices=[
                        create_choice(name="pip", value="pip"),
                        create_choice(name="master", value="master"),
                        create_choice(name="dev",value="dev")
                        ]),
               create_option(
                    name="clean",
                    description="Use pip-autoremove?",
                    option_type=5,
                    required=False
                ),
                create_option(
                    name="force",
                    description="Use --force-reinstall flag?",
                    option_type=5,
                    required=False
                ),
                create_option(
                    name="pip3",
                    description="Show pip3 intead of pip?",
                    option_type=5,
                    required=False
                )
             ]
        )
async def update(ctx, location: str, clean: bool = False, force: bool = False, pip3: bool = False):
    msg = ""
    if clean == True:
        msg += f"**Clean installation from `{location}`**\n - `pip install pip-autoremove`\n - `pip-autoremove spotdl -y`\n - `pip cache purge`"
    else:
        msg += f"**Update spotDL from `{location}`**\n - `pip uninstall spotdl`"
    
    if location == "pip" and clean == True:
        msg += "\n - `pip install -U spotdl`"
    elif location == "pip":
        msg = "`pip install -U spotdl`"
    elif location in ["dev", "master"]:
        msg += f"\n - `pip install -U https://codeload.github.com/spotDL/spotify-downloader/zip/{location}`"

    if force == True:
        msg = "`pip install -U --force-reinstall spotdl`"

    if pip3 == True:
        msg = msg.replace("pip ", "pip3 ")

    await ctx.send(content=msg)

@slash.slash(name="ffmpeg",
             description="FFmpeg issue FAQ",
             guild_ids=guild_ids,
             options=[
                 create_option(
                    name="not_found",
                    description="FFmpeg was not found?",
                    option_type=5,
                    required=False,
                 ),
                 create_option(
                     name="instructions",
                     description="Instructions for installing FFmpeg",
                     option_type=5,
                     required=False
                 ),
                 create_option(
                     name="no_detect",
                     description="FFmpeg versionn couldn't be detected?",
                     option_type=5,
                     required=False
                 ),
                 create_option(
                     name="specify_path",
                     description="Specify a path to your FFmpeg binary",
                     option_type=5,
                     required=False
                 )
             ]
             )
async def ffmpeg(ctx, not_found: bool = False, instructions: bool = False, no_detect: bool = False, specify_path: bool = False):
    embed = discord.Embed(title="FFmpeg and spotDL", description="spotDL requires FFmpeg v4.2 or above", color=discord.Color.blue())

    if not_found == True:
        embed.add_field(name="FFmpeg was not found, spotDL cannot continue?", value="spotDL either requires FFmpeg on PATH, or the binary to be specified via the -f flag.\nEnsure FFmpeg is installed!")
    if instructions == True:
        embed.add_field(name="Instructions to install FFmpeg", value="Windows: [Download Binaries](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) then [follow tutorial](https://windowsloop.com/install-ffmpeg-windows-10/)\n\
                                                                      OSX: `brew install ffmpeg`\nUbuntu:`sudo apt install ffmpeg -y`")    
    if no_detect == True:
        embed.add_field(name="FFmpeg version couldn't be detected?", value="Add the `--ignore-ffmpeg-version` flag to your spotDL command.\nThis is common if you are using a nightly FFmpeg build.", inline=False)
    if specify_path == True:
        embed.add_field(name="Specify a path to your FFmpeg binary?", value="Instead of adding FFmpeg to PATH, you can specify a path to the binary:\nAdd the `-f` or `--ffmpeg` flag to your command. e.g.\n`spotdl -f /path//to/ffmpeg.exe [trackUrl]`")
    elif not_found == False and instructions == False and no_detect == False and specify_path == False:
        embed.add_field(name="FFmpeg was not found, spotDL cannot continue?", value="spotDL either requires FFmpeg on PATH, or the binary to be specified via the -f flag.\nEnsure FFmpeg is installed!")
        embed.add_field(name="Instructions to install FFmpeg", value="Windows: [Download Binaries](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z) then [follow tutorial](https://windowsloop.com/install-ffmpeg-windows-10/)\n\
                                                                      OSX: `brew install ffmpeg`\nUbuntu:`sudo apt install ffmpeg -y`")    
        embed.add_field(name="Specify a path to your FFmpeg binary?", value="Instead of adding FFmpeg to PATH, you can specify a path to the binary:\nAdd the `-f` or `--ffmpeg` flag to your command. e.g.\n`spotdl -f /path//to/ffmpeg.exe [trackUrl]`")

    await ctx.send(embed=embed)

@slash.slash(name="version",
             description="Instructions for checking versions",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="app",
                     description="Instructions to check which app's version?",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(name="spotDL", value="spotDL"),
                         create_choice(name="FFmpeg", value="FFmpeg")
                     ]
                 ),
                create_option(
                    name="pip3",
                    description="Show pip3 intead of pip?",
                    option_type=5,
                    required=False
                )
             ])
async def version(ctx, app: str, pip3: bool = False):
    if app == "spotDL":
        msg = "**Check spotDL version**\n`pip show spotdl`"
    elif app == "FFmpeg":
        msg = "**Check FFmpeg version**\n`ffmpeg -version`"
    
    if pip3 == True:
        msg = msg.replace("pip ", "pip3 ")

    await ctx.send(content=msg)

@slash.slash(name="path",
             description="How to add things to PATH",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="shell",
                     description="What Shell is the user running? (Or Windows)",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(name="Windows", value="Windows"),
                         create_choice(name="zshrc", value="zshrc"),
                         create_choice(name="bashrc", value="bashrc")
                     ]
                 )
             ])
async def path(ctx, shell: str):
    if shell == "Windows":
        msg = "**Adding to PATH on Windows**\nIn Start Menu, Search `env` then click `Edit the system environment variables`, then click `Environment Variables` in the bottom right.\nIn System variables, scroll down to `Path` and double Click. You can now view or edit the PATH variable."
        
    elif shell == "zshrc":
        msg = "**Adding to PATH for Zsh terminal**\nAdd `export PATH=~/.local/bin:$PATH` at the bottom of `~/.zshrc`\nThen run `source ~/.zshrc`"
    elif shell == "bashrc":
        msg = "**Adding to PATH for Bash terminal**\nAdd `export PATH=~/.local/bin:$PATH` at the bottom of `~/.bashrc`\nThen run `source ~/.bashrc`"
    
    await ctx.send(content=msg)

@slash.slash(name="dl_branch",
             description="Removing &dl_branch=1 from URLs",
             guild_ids=guild_ids)
async def dl_branch(ctx):
    await ctx.send("**You must remove `&dl_branch=1` from URLs, since the `&` is a control operator in terminal**")

@slash.slash(name="outputformat",
             description="How to change output format? Options?",
             guild_ids=guild_ids)
async def outputformat(ctx):
    await ctx.send("**How to change output format?**\nUse the `-of` or `--output-format` flag.\nPossible formats are `mp3, ogg, flac, opus, m4a`\nE.g. `spotdl [trackUrl] -of opus`")

@slash.slash(name="certificates",
             description="Installing SSL certificates on OSX",
             guild_ids=guild_ids)
async def certificates(ctx):
    await ctx.send("On OSX? You need to install SSL certificates\nNavigate to `Applications/Python 3.9`, and double click `Install Certificates.command`\n(Change 3.9 to relavant version number)")

@slash.slash(name="download",
             description="Where did my files download?",
             guild_ids=guild_ids)
async def download(ctx):
    embed = discord.Embed(title="Where are my files downloaded? / How can I change download location?", color=0xFFFFFF)
    embed.add_field(name="By default, spotDL downloads to the Working Directory/Where you ran spotDL from", value="You can `cd` to the folder you want to run spotDL from", inline=False)
    embed.add_field(name="Changing output directory", value="Use the `-o` or `--output` flag to change output directory, e.g. `spotdl [trackUrl] -o /home/music/`", inline=False)
    embed.add_field(name="Windows Default & Tip", value="By default, Windows will download in `C:\\Users\\YOURNAME\\`.\n__Tip__\n`SHIFT +RIGHT CLICK` in desired folder and select \'Open Powershell Window Here\'", inline=False)
    embed.set_image(url="https://i.imgur.com/aDP8oEU.png")
    await ctx.send(embed=embed)

@slash.slash(name="testsong",
             description="spotDL command for our testsong",
             guild_ids=guild_ids)
async def testsong(ctx):
    await ctx.send("**Test Song:**\n`spotdl https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b`")

@slash.slash(name="install",
             description="Instructions on installing Python or spotDL",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="program",
                     description="What program to provide instructions for",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(name="spotDL", value="spotDL"),
                         create_choice(name="Python", value="Python"),
                         create_choice(name="FFmpeg", value="FFmpeg"),
                         create_choice(name="Termux", value="Termux")
                     ]
                 )
             ])
async def install(ctx, program: str):
    if program == "spotDL":
        msg = "**How to install spotDL?**\n*(Note: spotDL requires FFmpeg & Python)*\n\nRun `pip install spotdl` in a terminal"
    elif program == "Python":
        msg = "You need to install Python from <https://www.python.org/downloads/>\n\nEnsure to add to PATH when installing:\nhttps://i.imgur.com/jWq5EnV.png"
    elif program == "FFmpeg":
        msg = "**Installing FFmpeg:**\n\n**Windows:** Download binaries from <https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z> then follow this tutorial: <https://windowsloop.com/install-ffmpeg-windows-10/>.\n\
**OSX (M1):** <https://www.youtube.com/watch?v=wOZ7p7Zmz2s>\n**OSX (Other):** `brew install ffmpeg`\n**Ubuntu:** `sudo apt install ffmpeg -y`"
    elif program == "Termux":
        msg = "**spotDL has a dedicated Termux installation script.**\n`curl -L https://github.com/spotDL/spotify-downloader/raw/master/termux/setup_spotdl.sh | sh`\n\nspotDL will install at `/data/data/com.termux/files/usr/bin/spotdl/`, and **Songs download to `$HOME/storage/shared/songs`**"
    
    await ctx.send(msg)

@slash.slash(name="github",
             description="Links to different spotDL documentation",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="file",
                     description="What file do you want to link to?",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(name="readme", value="readme"),
                         create_choice(name="installguide", value="installguide"),
                         create_choice(name="contributing", value="contributing"),
                         create_choice(name="corevalues", value="corevalues"),
                         create_choice(name="license", value="license")
                     ]
                 )
             ])
async def github(ctx, file: str):
    if file == "readme":
        msg = "Detailed information in our README.md\n<https://github.com/spotDL/spotify-downloader/blob/master/README.md>"
    elif file == "installguide":
        msg = "Installation Guide at <https://github.com/spotDL/spotify-downloader/blob/master/docs/INSTALLATION.md>"
    elif file == "contributing":
        msg = "Contributing Guidelines at <https://github.com/spotDL/spotify-downloader/blob/master/docs/CONTRIBUTING.md>"
    elif file == "corevalues":
        msg = "Core Values at <https://github.com/spotDL/spotify-downloader/blob/master/docs/CORE_VALUES.md>"
    elif file == "license":
        msg = "Our License at <https://github.com/spotDL/spotify-downloader/blob/master/LICENSE>"
    
    await ctx.send(msg)

@slash.slash(name="quality",
             description="Info regarding audio quality & bitrate",
             guild_ids=guild_ids)
async def quality(ctx):
    await ctx.send("spotDL automatically gets the highest quality audio we can from YouTube.")

@slash.slash(name="ytmusic",
             description="YouTube Music being required",
             guild_ids=guild_ids)
async def ytmusic(ctx):
    await ctx.send("**YouTube Music must be available in your country for spotDL to work. This is because we use YouTube Music to filter search results. You can check if YouTube Music is available in your country, by visiting YouTube Music.** <https://music.youtube.com/>")

@slash.slash(name="fromyoutube",
             description="spotDL downloads from YouTube",
             guild_ids=guild_ids)
async def fromyoutube(ctx):
    await ctx.send("spotDL downloads from YouTube if a match is found. https://i.imgur.com/tCaTBTt.png")








@slash.slash(name="rules",
             description="Dev prompts for users to follow the rules.",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="rule",
                     description="Which prompt?",
                     option_type=3,
                     required=True,
                     choices=[
                         create_choice(name="reply", value="reply"),
                         create_choice(name="ping", value="ping"),
                         create_choice(name="channel", value="channel"),
                     ]
                 )
             ])
async def rules(ctx, rule: str):
    if rule == "reply":
        msg = "**Please disable reply pings**\n\nOur devs are human as well! Please wait patiently, we will reply as soon as we can.\nhttps://i.imgur.com/yIxI1RW.png"
    elif rule == "ping":
        msg = "**Please don't ping devs**\n\nOur devs are human as well! Please wait patiently, we will reply as soon as we can."
    elif rule == "channel":
        msg = "**Please don't spam your issue across channels**\n\nOur devs are human as well! Please wait patiently, we will reply as soon as we can."

    await ctx.send(msg)



@client.event
async def on_message(message):
    if "dll load failed" in message.content.lower():
        await message.reply("On Windows? You need to install Visual C++ 2019 redistributable\nhttps://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist")
    elif "unable to get audio stream" in message.content.lower():
        await message.reply("On OSX? You need to install SSL certificates\nNavigate to `Applications/Python 3.9`, and double click `Install Certificates.command`\n(Change 3.9 to relavant version number)")
    elif "tester123silver" in message.content:
        await message.reply("got you!")


# async def update(ctx, from: str):
#     await ctx.send("a")

# @slash.slash(name="Various install instructions",
#              description="",
#              guild_ids=guild_ids)
# async def _a(ctx):
#     await ctx.send("")

# @slash.slash(name="",
#              description="",
#              guild_ids=guild_ids)
# async def _a(ctx):
#     await ctx.send("")




client.run(discord_token)