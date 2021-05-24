# WWP Bot

import os
from datetime import datetime
from xml.sax.saxutils import escape, unescape

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name="search", help="Search for ids by title")
async def searchForTitle(ctx, term):
    results = searchByTitle(term)
    if len(results) == 0:
        embed=discord.Embed(title="No titles found", description="Sorry, no titles found containing: \"" + term + "\"")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Search results for: \"" + term + "\"", description=formatSearchResults(results) )
        await ctx.send(embed=embed)


@bot.command(name="vote", help="Vote for a title using its id")
async def voteForTitle(ctx, titleID):
    d = detailsFromID(titleID)

    if d == 0:
        embed=discord.Embed(title="Vote failed", description="Sorry, I don't recognize \"" + titleID + "\" as a title ID\rTry using the \"!search\" command to find the correct ID")
        await ctx.send(embed=embed)
    else:
        s = d.split(';')

        embed=discord.Embed(title="Added vote for \"" + s[1] + "\"", description="[" + s[2].upper().rstrip() + "] - " + s[0])
        file = discord.File("../images/pngs/" + titleID + ".png", filename="image.png")
        embed.set_thumbnail(url="attachment://image.png")

        writeVoteToFile(titleID)

        await ctx.send(file=file, embed=embed)

@bot.event
async def on_message(message):
    if not message.content:
        return
    elif message.author == bot.user:
        return
    elif message.content[0] == "!" :
        await bot.process_commands(message)
    elif message.content.strip() != "":
        ts = message.created_at
        st = ts.strftime('%Y-%m-%d %H:%M:%S')

        sanit = escape(unescape(message.content[:100].strip().strip(";;")))
        saname = escape(unescape(message.author.name[:20].strip().strip(";;")))
        with open("../text/msg.txt", "a") as f:
            f.write(st + ";;" + sanit + ";;" + saname +"\r")


# helper functions
# Vote functions
# Write titleID to file for vote tallying
def writeVoteToFile(titleID):
    with open("../text/vote.txt", "a") as f:
        f.write(titleID + "\r")


# Printing functions
def formattedStringfromResult(result):
    s = result.rstrip().split(';')
    f = "\"" + s[1] + "\" [" + s[2].upper() + "] - " + s[0]
    return f

def formatSearchResults(results):
    s = []
    for r in results:
        s.append(formattedStringfromResult(r))

    return "\n".join(s)


# Searching functions
def searchByTitle(term):
    results = []

    with open("../text/titleinfo.txt") as f:
        for line in f:
            if term.upper() in line.upper():
                results.append(line)
            if len(results) > 5 :
                return results

    return results


def detailsFromID(titleID):
    with open("../text/titleinfo.txt") as f:
        for line in f:
            if line[8:16] == titleID[8:16]:
                return line
    return 0

def titleFromID(titleID):
    d = detailsFromID(titleID)
    s = d.split(';')
    return s[1]


bot.run(TOKEN)