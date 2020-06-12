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


def isPrime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


class Mathematics(commands.Cog):
    @commands.command(description="Square a number.",
                      brief="Square a number",
                      aliases=['pow2', 'selfmult', 'sq'],
                      pass_context=True)
    async def square(self, ctx, number: float = None):
        if number is None:
            await ctx.send("Proper format for command: !square <number>.")
        else:
            result = number * number
            await ctx.send(result)

    @square.error
    async def square_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'square'.\nProper format for command: !square <number>.")

    @commands.command(description="Add two numbers.",
                      brief="Add two numbers",
                      aliases=['addition', 'addup', 'plus', 'sum'],
                      pass_context=True)
    async def add(self, ctx, number1: float = None, number2: float = None):
        if number1 is None or number2 is None:
            await ctx.send("Proper format for command: !add <first number> <second number>.")
        else:
            result = number1 + number2
            await ctx.send(result)

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'add'.\nProper format for command: !add <first number> <second number>.")

    @commands.command(description="Get the sum of a list of numbers.",
                      brief="Add multiple values",
                      pass_context=True)
    async def total(self, ctx, *values: float):
        if len(values) < 1:
            await ctx.send("Proper format for command: !total <val1> <val2> ... <valx>.")
            return
        res = 0
        for x in values:
            res += x
        await ctx.send(res)

    @total.error
    async def total_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'total'.\nProper format for command: !total <val1> <val2> ... <valx>.")

    @commands.command(description="Calculate factorials.",
                      brief="Calculate factorials",
                      pass_context=True)
    async def factorial(self, ctx, value: int):
        if value < 0:
            await ctx.send("Factorial only works for integers greater than or equal to 0.")
        elif value == 0:
            await ctx.send(1)
        else:
            res = 1
            for i in range(2, value + 1):
                res *= i

            ans = str(res)
            if len(ans) > 2000:
                await ctx.send("Because this factorial is far too long, it will be privately sent to you.")
                outputs = []
                index = 0
                pre = 0
                while index < len(ans):
                    index += 1
                    if index % 2000 == 0:
                        outputs.append(ans[pre: index - 1])
                        pre = index
                outputs.append(ans[pre:])

                for x in outputs:
                    await ctx.author.send(x)
            else:
                await ctx.send(ans)

    @factorial.error
    async def factorial_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'factorial'.\nProper format for command: !factorial <value>.")

    @commands.command(description="Add two numbers.",
                      brief="Subtract two numbers",
                      aliases=['subtract', 'minus', 'diff'],
                      pass_context=True)
    async def sub(self, ctx, number1: float = None, number2: float = None):
        if number1 is None or number2 is None:
            await ctx.send("Proper format for command: !sub <first number> <second number>.")
        else:
            result = number1 - number2
            await ctx.send(result)

    @sub.error
    async def sub_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'sub'.\nProper format for command: !sub <first number> <second number>.")

    @commands.command(description="Multiply two numbers.",
                      brief="Multiply two numbers",
                      aliases=['multiply', 'times', 'product', 'prod'],
                      pass_context=True)
    async def mult(self, ctx, number1: float = None, number2: float = None):
        if number1 is None or number2 is None:
            await ctx.send("Proper format for command: !mult <first number> <second number>.")
        else:
            result = number1 * number2
            await ctx.send(result)

    @mult.error
    async def mult_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'mult'.\nProper format for command: !mult <first number> <second number>.")

    @commands.command(
        description="Divide two numbers with specified precision. If no precision is specified, default is 2.",
        brief="Divide two numbers",
        aliases=['divide', 'quotient', 'fraction', 'frac'],
        pass_context=True)
    async def div(self, ctx, number1: float = None, number2: float = None, precision: int = 2):
        if number1 is None or number2 is None:
            await ctx.send("Proper format for command: !div <first number> <second number> <precision (optional)>.")
        if number2 == 0:
            await ctx.send("Cannot divide by zero.")
        else:
            result = round(number1 / number2, precision)
            await ctx.send(result)

    @div.error
    async def div_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'div'.\nProper format for command: !div <first number> <second number> <precision (optional)>.")

    @commands.command(description='Get the value of a number raised to an exponent.',
                      brief="Exponents",
                      aliases=['exp', 'power', 'raiseto'],
                      pass_contet=True)
    async def pwr(self, ctx, base: float = None, exponent: float = None):
        if base is None or exponent is None:
            await ctx.send("Proper format for command: !pow <base> <exponent>.")
        else:
            result = base ** exponent
            await ctx.send(result)

    @pwr.error
    async def pwr_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'pwr'.\nProper format for command: !pwr <base> <exponent>.")

    @commands.command(description="Prime factorize a number.",
                      brief="Prime factorization",
                      aliases=['pfact', 'primefactorize'],
                      pass_context=True)
    async def pfactor(self, ctx, value: int = None):
        if isPrime(value):
            await ctx.send("That is a prime number.")
            return

        old = value
        nOcc = 0
        factorized = {}
        while value % 2 == 0:
            nOcc += 1
            value /= 2

        if nOcc > 0:
            factorized.update({2: nOcc})

        fact = 3
        while value > 1:
            occ = 0
            if isPrime(fact):
                while value % fact == 0:
                    value /= fact
                    occ += 1

                if occ > 0:
                    factorized.update({fact: occ})
            fact += 2

        output = ""
        for factor, occurences in factorized.items():
            if occurences != 1:
                output += str(factor) + "^" + str(occurences) + " x "
            else:
                output += str(factor) + " x "

        output = output[0:len(output) - 2]
        await ctx.send(str(old) + " prime factorized: " + output)

    @pfactor.error
    async def pfactor_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'pfactor'.\nProper format for command: !pfactor <value>.")

    @commands.command(description="Calculate logarithms.",
                      brief="Calculate logarithms",
                      aliases=['logarithm'],
                      pass_context=True)
    async def log(self, ctx, base: float = None, value: float = None):
        if base is None and value is None:
            await ctx.send("Proper format for command: !log <base> <value>.")
            return
        elif base is not None and value is None:
            value = base
            base = 10
        if base <= 0 or value <= 0:
            await ctx.send("Cannot compute logarithm for the given values.")
            return

        output: str = str(round(math.log10(value) / math.log10(base), 7))
        await ctx.send(output)

    @log.error
    async def log_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'log'.\nProper format for command: !log <base> <value>.")

    @commands.command(
        description="Permutation calculator. Only integer values greater than or equal to 0 are permitted.",
        brief="n permute r",
        aliases=['permute', 'npr'],
        pass_context=True)
    async def nPr(self, ctx, n: int = None, r: int = None):
        if n is None or r is None:
            await ctx.send("Proper format for command: !nPr <n> <r>.")
            return

        if n < r:
            await ctx.send("n must be greater than or equal to r.")
            return

        if n < 0 or r < 0:
            await ctx.send("Values must not be less than 0.")
            return

        numerator = 1
        denominator = 1
        for i in range(2, n + 1):
            numerator *= i

        for j in range(2, n - r + 1):
            denominator *= j

        ans: int = int(numerator / denominator)
        output = str(ans)
        await ctx.send("P(" + str(n) + ", " + str(r) + ") = " + output)

    @nPr.error
    async def nPr_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument detected for command 'nPr'.\nProper format for command: !nPr <n> <r>.")

    @commands.command(
        description="Combinations calculator. Only integer values greater than or equal to 0 are permitted.",
        brief="n choose r",
        aliases=['choose', 'ncr'],
        pass_context=True)
    async def nCr(self, ctx, n: int = None, r: int = None):
        if n is None or r is None:
            await ctx.send("Proper format for command: !nPr <n> <r>.")
            return

        if n < r:
            await ctx.send("n must be greater than or equal to r.")
            return

        if n < 0 or r < 0:
            await ctx.send("Values must not be less than 0.")

        nFactorial = 1
        rFactorial = 1
        nMrFactorial = 1

        for i in range(2, n + 1):
            nFactorial *= i
        for j in range(2, r + 1):
            rFactorial *= j
        for k in range(2, n - r + 1):
            nMrFactorial *= k

        ans: int = int(nFactorial / (rFactorial * nMrFactorial))
        output = str(ans)
        await ctx.send("C(" + str(n) + ", " + str(r) + ") = " + output)

    @nCr.error
    async def nCr_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument detected for command 'nCr'.\nProper format for command: !nCr <n> <r>.")

    @commands.command(description="Convert decimal to binary.",
                      brief="Decimal to binary",
                      aliases=['bin'],
                      pass_context=True)
    async def binary(self, ctx, value: int = None):
        if value is None:
            await ctx.send("No value detected for conversion.")
            return

        await ctx.send(bin(value).replace("0b", ""))

    @binary.error
    async def binary_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'binary'.\nProper format for command: !binary <value>.")

    @commands.command(description="Convert decimal to hexadecimal.",
                      brief="Decimal to hexadecimal",
                      aliases=['hexa', 'hexadecimal'],
                      pass_context=True)
    async def hexadec(self, ctx, value: int = None):
        if value is None:
            await ctx.send("No value detected for conversion.")
            return

        converted = str(hex(value).replace("0x", ""))
        output = ""
        for i in range(len(converted)):
            output += converted[i].upper()

        await ctx.send(output)

    @hexadec.error
    async def hexadec_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'hexadec'.\nProper format for command: !hexadec <value>.")

    @commands.command(description="Convert decimal to octal.",
                      brief="Decimal to octal",
                      pass_context=True)
    async def octal(self, ctx, value: int = None):
        if value is None:
            await ctx.send("No value detected for conversion.")
            return

        await ctx.send(oct(value).replace("0o", ""))

    @octal.error
    async def octal_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument detected for command 'octal'.\nProper format for command: !octal <value>.")

    @commands.command(description="Convert number of base n numeral system back to decimal.",
                      brief="Convert back to decimal",
                      aliases=['dec', 'deci'],
                      pass_context=True)
    async def decimal(self, ctx, value: str = None, base: int = None):
        if value is None or base is None:
            await ctx.send("Proper format for command: !decimal <value> <base n>.")
            return
        await ctx.send(int(value, base))

    @decimal.error
    async def decimal_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                "Invalid argument detected for command 'decimal'.\nProper format for command: !decimal <value> <base n>.")


def setup(client):
    client.add_cog(Mathematics(client))
