# Work with Python 3.6
import random
from random import randrange
import asyncio
import aiohttp
import json
import discord
from timeit import default_timer as timer
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands


class Randomizers(commands.Cog):
    @commands.command(description="Get a definite answer.",
                      brief="Got a question?",
                      aliases=['8ball', 'magicanswer', '8Ball'],
                      pass_context=True)
    async def eightball(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("You didn't ask a question.")
            return

        possible_responses = [
            'It is very much certain.',
            'It is possible',
            'It is unclear at this time',
            'Definitely not',
            'Not too likely'
        ]
        await ctx.send(random.choice(possible_responses) + " " + ctx.author.mention)

    @commands.command(description="Flip a coin! By default, flips a coin a single time.",
                      brief="Coinflipper",
                      aliases=['cflip'],
                      pass_context=True)
    async def coinflip(self, ctx, times: int = 1):
        res = ""
        numH = 0
        numT = 0
        if times <= 1950:
            for i in range(times):
                flip = randrange(10000)
                if flip % 2 == 0:
                    res += "H"
                    numH += 1
                else:
                    res += "T"
                    numT += 1
            await ctx.send(res + " " + ctx.author.mention)
            await ctx.send(
                "Number of heads: " + str(numH) + ". Number of tails: " + str(numT) + ". " + ctx.author.mention)
        else:
            await ctx.send("Maximum flip limit exceeded. The limit is 200. " + ctx.author.mention)

    @coinflip.error
    async def cflip_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Non-numerical argument detected for command 'coinflip'. Please provide a numerical value or none at all for a single coin flip.")

    @commands.command(description="Pick a random number in a given range.",
                      brief="Random number generator",
                      aliases=['rng', 'RNG', 'randomnumber', 'randomnum'],
                      pass_context=True)
    async def randnum(self, ctx, lower: int = None, upper: int = None):
        if lower is None or upper is None:
            await ctx.send("Proper format for command: !randnum <lower bound> <upper bound>.")
        elif lower > upper:
            await ctx.send(
                "I asked you to give me the lower number first, and yet you fail to understand that " + ctx.author.mention + ".")
            temp = lower
            lower = upper
            upper = temp
        await ctx.send(randrange(lower, upper))

    @randnum.error
    async def randnum_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'pwr'.\nProper format for command: !randnum <lower bound> <upper bound>.")

    @commands.command(description="Settle once and for all which choice is better! Use quotations"
                                  " for multiple word elements.",
                      brief="Compare two choices",
                      aliases=['comp'],
                      pass_context=True)
    async def compare(self, ctx, elem1=None, elem2=None):
        if elem1 is None or elem2 is None:
            await ctx.send("Proper format for command: !compare <first element> <second element>.")
        else:
            det = randrange(100)
            if det % 2 == 0:
                await ctx.send(elem1 + " is better than " + elem2 + " " + ctx.author.mention + ".")
            else:
                await ctx.send(elem2 + " is better than " + elem1 + " " + ctx.author.mention + ".")

    @commands.command(description="Can't make a choice? Ask me!",
                      brief="Randomly choose",
                      aliases=['decide', 'pick', 'randomchoice', 'rc'],
                      pass_context=True)
    async def randchoice(self, ctx, *choices: str):
        if len(choices) < 1:
            await ctx.send("No choices detected.")
            return
        await ctx.send("The chosen item is: " + random.choice(choices) + ".")


def setup(client):
    client.add_cog(Randomizers(client))
