# WWP Bot

import os

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
        embed=discord.Embed(title="No titles found", description="Sorry, no titles found containing: " + term + "\"")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Search results for: \"" + term + "\"", description=formatSearchResults(results) )
        await ctx.send(embed=embed)


@bot.command(name="vote", help="Vote for a title using its id")
async def voteForTitle(ctx, titleID):
    d = detailsFromID(titleID)
    s = d.split(';')

    embed=discord.Embed(title=s[1], description="Added vote for \"" + s[1] + "\"")
    embed.set_footer(text= s[2].upper() + " region - id:" + s[0])
    file = discord.File("../images/pngs/" + titleID + ".png", filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")
    await ctx.send(file=file, embed=embed)



# helper functions
def formattedStringfromResult(result):
    s = result.split(';')
    f = "\"" + s[1] + "\" - " + s[2].upper() + " - id: " + s[0]
    return f

def formatSearchResults(results):
    s = []
    for r in results:
        s.append(formattedStringfromResult(r))

    return "\n".join(s)


def searchByTitle(term):
    results = []

    with open("../text/titleinfo") as f:
        for line in f:
            if term in line:
                results.append(line)
            if len(results) > 4 :
                return results

    return results


def detailsFromID(titleID):
    with open("../text/titleinfo") as f:
        for line in f:
            if line[0:16] == titleID:
                return line
    return "not found"

def titleFromID(titleID):
    d = detailsFromID(titleID)
    s = d.split(';')
    return s[1]


bot.run(TOKEN)