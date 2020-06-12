# Work with Python 3.6
import random
from random import randrange
import asyncio
import aiohttp
import json
import discord
import discord.ext.commands
import time
import math
import sys
from timeit import default_timer as timer
from discord import Game
from discord.ext.commands import Bot
from discord.ext import commands
from main import client

# JSON data containers
userBal = {str: float}

# Users in the game
joined = []


def balance_load():
    global userBal
    with open('userBal.json') as uBFile:
        userBal = json.load(uBFile)


def balance_dump():
    global userBal
    with open('userBal.json', 'w') as uBFile:
        json.dump(userBal, uBFile)


class Economy(commands.Cog):
    @commands.command(description="Check a user's balance.",
                      brief="Check a user's balance",
                      pass_context=True)
    async def bal(self, ctx, user: discord.Member = None):
        balance_load()
        if user is None:
            user = ctx.author

        output = ""
        if str(user.id) not in userBal.keys():
            userBal.update({str(user.id): 1000})

        output += user.display_name + "'s balance is $" + str(userBal[str(user.id)])
        await ctx.send(output)
        balance_dump()

    @bal.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that user.")

    @commands.command(description="Pay another member.",
                      brief="Make a payment",
                      pass_context=True)
    async def pay(self, ctx, recipient: discord.Member = None, amount: float = None):
        if recipient is None or amount is None:
            await ctx.send("Proper format for command: !pay <recipient>.")
            return

        if amount <= 0:
            await ctx.send("Payments must be greater than $0.00.")

        amount = round(amount, 2)
        balance_load()
        if str(ctx.author.id) not in userBal.keys():
            userBal.update({str(ctx.author.id): 1000})
        if str(recipient.id) not in userBal.keys():
            userBal.update({str(recipient.id): 1000})

        if userBal[str(ctx.author.id)] < amount:
            await ctx.send("You do not have sufficient funds to make this payment.")
            return

        userBal[str(ctx.author.id)] -= amount
        userBal[str(recipient.id)] += amount

        balance_dump()
        await ctx.send("Payment successful. Your new balance is $" + str(userBal[str(ctx.author.id)]))

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Incorrect command format. Try !pay <recipient> <amount>.")

    @commands.command(description="See the richest users.",
                      brief="See the richest users",
                      pass_context=True)
    async def baltop(self, ctx):
        global userBal
        balance_load()
        userBal = {k: v for k, v in sorted(userBal.items(), key=lambda item: item[1], reverse=True)}
        output = "**TOP BALANCES**\n-----------------------------------------------\n"
        idx = 1;
        for user, balance in userBal.items():
            USER = client.get_user(int(user))
            output += str(idx) + ". " + USER.display_name + ": $" + str(balance) + "\n"
            idx += 1

        await ctx.send(output)


def setup(client):
    client.add_cog(Economy(client))
