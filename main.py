# Work with Python 3.6
# USED IMPORTS
import random
from random import randrange
import asyncio
from discord.ext.commands import Bot
import json
import discord
import discord.ext.commands
import sys
from timeit import default_timer as timer

# Prefixes
BOT_PREFIX = ("!")

# Get at discordapp.com/developers/applications/me
TOKEN = ""


# Math quiz variables
quizzing = False
baseQuizScore = 1
quizSuccessScore = 1
quizStartTime = 0
quizEndTime = 0
ans = 0.00

# Type test variables
typing = False
typeStartTime = 0
typeEndTimes = 0
typeString = ""

# Easier type test variables
easyTyping = False
easyTypeStartTime = 0
easyTypeEndTime = 0
easyTypeString = "The quick brown fox jumps over the lazy dog."


# Containers of alphanumeric characters
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z',
         '1', '2', '3', '4', '5', '6', '7', '8', '9']
lChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z']
digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# JSON data containers
data = {'killer': []}
quizData = {str: int}
typetestData = {str: float}
ettData = {str: float}
levelRecords = [None] * 10
levelRecordHolders = [None] * 10
userLevel = {str: int}
userXp = {str: int}

# Pre-execution configurations
client = Bot(command_prefix=BOT_PREFIX)
client.load_extension('Mathematics')
client.load_extension('Randomizers')
client.load_extension('Economy')


# Utility function to load all JSON data files
def fileLoad():
    global quizData
    global levelRecords
    global levelRecordHolders
    global typetestData
    global ettData
    global data
    global userXp
    global userLevel
    with open('quizData.json') as qDFile:
        quizData = json.load(qDFile)
    with open('quizLevelRecordHolders.json') as qLRFile:
        levelRecordHolders = json.load(qLRFile)
    with open('quizLevelRecords.json') as qLFile:
        levelRecords = json.load(qLFile)
    with open('typetestRecords.json') as ttRFile:
        typetestData = json.load(ttRFile)
    with open('data.json') as dFile:
        data = json.load(dFile)
    with open('easyTypeTestRecords.json') as ettRFile:
        ettData = json.load(ettRFile)
    with open('userLevel.json') as uLFile:
        userLevel = json.load(uLFile)
    with open('userXp.json') as uXFile:
        userXp = json.load(uXFile)


# Utility function to dump into JSON files
def fileDump():
    global quizData
    global levelRecords
    global levelRecordHolders
    global typetestData
    global ettData
    global data
    global userXp
    global userLevel
    with open('quizData.json', 'w') as qDFile:
        json.dump(quizData, qDFile)
    with open('quizLevelRecordHolders.json', 'w') as qLRFile:
        json.dump(levelRecordHolders, qLRFile)
    with open('quizLevelRecords.json', 'w') as qLFile:
        json.dump(levelRecords, qLFile)
    with open('typetestRecords.json', 'w') as ttRFile:
        json.dump(typetestData, ttRFile)
    with open('data.json', 'w') as dFile:
        json.dump(data, dFile)
    with open('easyTypeTestRecords.json', 'w') as ettRFile:
        json.dump(ettData, ettRFile)
    with open('userXp.json', 'w') as uXFile:
        json.dump(userXp, uXFile)
    with open('userLevel.json', 'w') as uLFile:
        json.dump(userLevel, uLFile)

async def updateLevel(xp: int, member: discord.Member, channel: discord.TextChannel):
    global userLevel
    global userXp
    fileLoad()
    if str(member.id) not in userLevel.keys():
        userXp.update({str(member.id): xp})
        userLevel.update({str(member.id): 1})
    else:
        userXp[str(member.id)] += xp
        if userXp[str(member.id)] >= 10000:
            userLevel[str(member.id)] += 1
            userXp[str(member.id)] -= 10000
            await channel.send("Congratulations " + member.mention + ", you leveled up to Level " + str(userLevel[str(member.id)]))
    fileDump()

@client.event
async def on_ready():
    channel = client.get_channel(705242699623563304)
    print("Logged in as " + client.user.name)
    fileLoad()
    for ident in data['killer']:
        user = client.get_user(ident['id'])
    await channel.send("**-------------------------------------**\n"
                       "**I AM ONLINE**\nI was previously killed by **" + user.display_name +
                       "**\n**-------------------------------------**")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Die Hard"))


@client.command(description='Dab on them.',
                brief='Dab',
                aliases=['DAB'],
                pass_context=True)
async def dab(ctx):
    await ctx.send("https://gfycat.com/dirtylamefantail")


@client.command(description="Create a randomly generated math quiz of the specified difficulty (integer from 1-10).",
                brief="Challenge your math skills",
                aliases=['test', 'challenge'],
                pass_context=True)
async def quiz(ctx, difficulty: int = 2):
    global quizzing
    global quizStartTime
    global quizSuccessScore
    global baseQuizScore

    if quizzing:
        await ctx.send("Can't start a new quiz until the previous one is solved!")
    else:
        opsB = ['+', '-']
        if difficulty > 10:
            difficulty = 10
        elif difficulty < 1:
            difficulty = 1

        val1: int = 0
        val2: int = 0
        quizSuccessScore = difficulty

        if difficulty == 1:
            val1 = randrange(10) + 1
            val2 = randrange(10) + 1
            choseOp = '*'
        elif difficulty == 2:
            val1 = randrange(100) + 1
            val2 = randrange(100) + 1
            choseOp = random.choice(opsB)
        elif difficulty == 3:
            choice = randrange(100)
            if choice % 2 == 0:
                val1 = randrange(10, 100)
                val2 = randrange(10) + 1
                choseOp = '*'
            else:
                val1 = randrange(100, 1000)
                val2 = randrange(10, 100)
                choseOp = random.choice(opsB)
        elif difficulty == 4:
            choice = randrange(100)
            if choice % 2 == 0:
                val1 = randrange(100, 1000)
                val2 = randrange(100, 1000)
                choseOp = random.choice(opsB)
            else:
                val1 = randrange(10, 100)
                val2 = randrange(10, 100)
                choseOp = '*'
        elif difficulty == 5:
            val1 = randrange(1000, 10000)
            val2 = randrange(1000, 10000)
            choseOp = random.choice(opsB)
        elif difficulty == 6:
            val1 = randrange(100, 1000)
            val2 = randrange(10, 100)
            choseOp = '*'
        elif difficulty == 7:
            val1 = randrange(10000, 100000)
            val2 = randrange(10000, 100000)
            choseOp = random.choice(opsB)
        elif difficulty == 8:
            val1 = randrange(100, 1000)
            val2 = randrange(10, 100)
            choseOp = '%'
        elif difficulty == 9:
            val1 = randrange(1000, 10000)
            val2 = randrange(10, 1000)
            choseOp = '%'
        elif difficulty == 10:
            val1 = randrange(10000, 1000000)
            val2 = randrange(10, 1000)
            choseOp = '%'

        quizzing = True
        global ans

        if choseOp == '+':
            await ctx.send("What is " + str(val1) + " + " + str(val2) + "?")
            ans = int(val1 + val2)
        elif choseOp == '-':
            ans = int(val1 - val2)
            await ctx.send("What is " + str(val1) + " - " + str(val2) + "?")
        elif choseOp == '*':
            ans = int(val1 * val2)
            await ctx.send("What is " + str(val1) + " x " + str(val2) + "?")
        elif choseOp == '%':
            ans = int(val1 % val2)
            await ctx.send("What is " + str(val1) + " % (mod) " + str(val2) + "?")

        quizStartTime = timer()


@quiz.error
async def quiz_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send("Invalid difficulty level detected for quiz. Please provide a numerical difficulty value from 1-10.")


@client.command(description="Get quiz level time records.",
                brief="Quiz time records",
                aliases=['qtr'],
                pass_context=True)
async def quiztimerecords(ctx):
    global levelRecords
    global levelRecordHolders
    fileLoad()
    output = "**QUIZ LEVEL TIME RECORDS**\n-----------------------------------------------\n"
    for i in range(0, len(levelRecords)):
        output += "Level " + str(int(i + 1)) + ": " + str(levelRecords[i]) + "s"
        if levelRecordHolders[i] == 0 or levelRecordHolders[i] is None:
            output += ", held by no one\n"
        else:
            holder = client.get_user(levelRecordHolders[i])
            output += ", held by **" + holder.display_name + "**\n"

    await ctx.send(output + "-----------------------------------------------\n")


@client.command(description="Get quiz leaderboards.",
                brief="Quiz leaderboards",
                aliases=['quizstat', 'ql', 'QL'],
                pass_context=True)
async def quizlead(ctx):
    global quizData
    fileLoad()

    quizData = {k: v for k, v in sorted(quizData.items(), key=lambda item: item[1], reverse=True)}
    output = "**QUIZ LEADERBOARDS**\n-----------------------------------------------\n"
    for user, score in quizData.items():
        USER = client.get_user(int(user))
        output += USER.display_name + ": " + str(score) + "\n"

    await ctx.send(output + "-----------------------------------------------\nLeaderboard is based on score.")


@client.command(description="Generate a random string for a typing test!",
                brief="Type speed test",
                aliases=['tt'],
                pass_context=True)
async def typetest(ctx):
    global typing
    global typeStartTime
    global typeString
    if typing:
        await ctx.send("Can't start a new type test until the previous one is terminated (use 'TERMINATE')!")
        return

    typing = True
    typeStartTime = timer()
    typeString = ""

    for i in range(0, 20):
        typeString += random.choice(lChars)

    output = ""
    for i in range(len(typeString)):
        output += typeString[i] + " "

    await ctx.send(
        "Type this string BACKWARDS (without spaces) as fast as you can: **" + output + "**\nTo end this test, type 'TERMINATE'.")
    temp = typeString[::-1]
    typeString = temp


@client.command(description="Get the typing test records.",
                brief="Typing test records",
                aliases=['tr', 'tl'],
                pass_context=True)
async def typeRecords(ctx):
    global typetestData
    fileLoad()

    typetestData = {k: v for k, v in sorted(typetestData.items(), key=lambda item: item[1], reverse=True)}
    output = "**TYPETEST LEADERBOARDS**\n-----------------------------------------------\n"
    for user, cpm in typetestData.items():
        USER = client.get_user(int(user))
        output += USER.display_name + ": " + str(cpm) + "CPM\n"

    await ctx.send(output + "-----------------------------------------------\nLeaderboard is based on CPM. Negative scores denote cheaters.")

@client.command(description="Another, easier variant of the typing test with its own leaderboards.",
                brief="Easier typing test",
                aliases=['ett'],
                pass_context=True)
async def easytypetest(ctx):
    global easyTyping
    global easyTypeStartTime

    if easyTyping:
        await ctx.send("Can't start a new type test until the previous one is terminated (use 'TERMINATE')!")
        return

    easyTyping = True
    easyTypeStartTime = timer()
    await ctx.send("Type 'The quick brown fox jumps over the lazy dog.' as fast as you can.")

@client.command(description="Easier type test leaderboards.",
                brief="Easier type test leaderboards",
                pass_context=True)
async def etr(ctx):
    global ettData
    fileLoad()

    ettData = {k: v for k, v in sorted(ettData.items(), key=lambda item: item[1], reverse=False)}
    output = "**EASIER TYPETEST LEADERBOARDS**\n-----------------------------------------------\n"
    for user, time in ettData.items():
        USER = client.get_user(int(user))
        output += USER.display_name + ": " + str(time) + "s\n"

    await ctx.send(output + "-----------------------------------------------\nLeaderboard is based on time.")

@client.command(description="tRanSLaTe yOuR teXT inTO tHIS.",
                brief="tRanSLaTe yOuR teXT inTO tHIS",
                aliases=['wt'],
                pass_context=True)
async def weirdText(ctx, *words):
    if len(words) < 1:
        await ctx.send("Give me a phrase to translate.")
        return
    res = ""
    for word in words:
        for i in range(len(word)):
            case = randrange(100)
            if case % 2 == 0:
                res += word[i].lower()
            else:
                res += word[i].upper()
        res += " "
    await ctx.send(res)


@client.command(description="Encrypt a message.",
                brief="Encrypt a message",
                aliases=['encode', 'enc'],
                pass_context=True)
async def encrypt(ctx, *phrase):
    key = ""
    for i in range(7):
        key += random.choice(digits)

    output = ""
    keyIndex = 0
    for word in phrase:
        for i in range(len(word)):
            index = 0
            while chars[index] != word[i]:
                index += 1
                if index >= len(chars):
                    break

            if index >= len(chars):
                output += word[i]
                continue

            index += int(key[keyIndex])
            if index >= 61:
                index -= 61
            output += chars[index]

            keyIndex += 1
            if keyIndex >= 7:
                keyIndex = 0

        output += " "
    await ctx.author.send("Encrypted message: " + output + "\nKey: " + key)


@client.command(description="Decrypt an encrypted message with a given 7-digit encryption key.",
                brief="Decrypt a message",
                aliases=['decode', 'decr'],
                pass_context=True)
async def decrypt(ctx, *data):
    if len(data) < 2:
        await ctx.send("Insufficient data provided. Proper format for command: !decrypt <phrase> <key>.")
        return
    key = data[len(data) - 1]
    if len(key) < 7:
        await ctx.send("That is not a 7-digit encryption key.")
        return

    for i in range(len(key)):
        if not key[i].isdigit:
            await ctx.send(
                "Invalid key provided. Keys can only contain numerical characters. Proper format for command: !decrypt <phrase> <key>.")
            return

    output = ""
    keyIndex = 0
    for word in data:
        if word != key:
            for i in range(len(word)):
                index = 0

                while chars[index] != word[i]:
                    index += 1
                    if index >= len(chars):
                        break

                if index >= len(chars):
                    output += word[i]
                    continue

                index -= int(key[keyIndex])
                if index < 0:
                    index += 61
                output += chars[index]

                keyIndex += 1
                if keyIndex >= 7:
                    keyIndex = 0
            output += " "
    await ctx.author.send("Decrypted message: " + output)


@client.command(description="Get a user's stats.",
                brief="User stats",
                pass_context=True)
async def stats(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    fileLoad()
    output = "-----------------------------------------------\n**" + member.display_name + "'s statistics**\n-----------------------------------------------\nUser Level: "
    if str(member.id) in userLevel.keys():
        output += str(userLevel[str(member.id)]) + "\n"
    else:
        output += "nothing yet\n"

    output += "XP: "
    if str(member.id) in userXp.keys():
        output += str(userXp[str(member.id)]) + " / 10000\n"
    else:
        output += "0 / 10000\n"

    output += "Quiz Score: "
    if str(member.id) in quizData.keys():
        output += str(quizData[str(member.id)]) + "\n"
    else:
        output += "nothing yet\n"

    output += "Regular Typing Test Record CPM: "
    if str(member.id) in typetestData.keys():
        output += str(typetestData[str(member.id)]) + " CPM\n"
    else:
        output += "none yet\n"

    output += "Easier Typing Test Record Time: "
    if str(member.id) in ettData.keys():
        output += str(ettData[str(member.id)]) + "s\n"
    else:
        output += "none yet\n"

    output += "-----------------------------------------------\n"
    await ctx.send(output)

@stats.error
async def stats_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send("Cannot find that user in my databases.")





@client.event
async def on_message(message):
    await client.process_commands(message)
    global quizzing
    global quizStartTime
    global quizEndTime
    global typing
    global typeString
    global typeEndTimes
    global data
    global quizData
    global quizSuccessScore
    global easyTyping
    global easyTypeStartTime
    global easyTypeEndTime
    global userLevel
    global userXp

    if message.content == "TERMINATE":
        if quizzing:
            await message.channel.send("Did you really just give up? That's sad. The answer was: " + str(ans) + ". Try harder next time.")
            quizzing = False
        elif typing or easyTyping:
            typing = False
            easyTyping = False
            await message.channel.send("Typing test terminated.")
    elif quizzing and not message.author.bot and message.content.find("!quiz") == -1:
        decimalIndex = message.content.find('.')
        if message.content == str(ans):
            quizzing = False
            quizEndTime = timer()
            await message.channel.send("Correct! " + message.author.mention + ". It took you " + str(round(quizEndTime - quizStartTime, 3)) +
                                       "s to solve this problem! You have been awarded " + str(quizSuccessScore) + " points and earned " + str(quizSuccessScore * 100) + "XP.")

            await updateLevel(quizSuccessScore * 100, message.author, message.channel)

            if str(message.author.id) in quizData:
                quizData[str(message.author.id)] += quizSuccessScore
            else:
                quizData.update({message.author.id: 1})

            if levelRecords[quizSuccessScore - 1] is None:
                levelRecords[quizSuccessScore - 1] = round(quizEndTime - quizStartTime, 3)
                levelRecordHolders[quizSuccessScore - 1] = message.author.id
                await message.channel.send(message.author.mention + ", you beat the time record for level " + str(quizSuccessScore) + ".")
            elif levelRecords[quizSuccessScore - 1] > round(quizEndTime - quizStartTime, 3):
                levelRecords[quizSuccessScore - 1] = round(quizEndTime - quizStartTime, 3)
                levelRecordHolders[quizSuccessScore - 1] = message.author.id
                await message.channel.send(message.author.mention + ", you beat the time record for level " + str(quizSuccessScore) + ".")
            fileDump()
        elif message.content.isdigit() or \
                message.content[1:].isdigit() or \
                (message.content[0:decimalIndex].isdigit() and
                 message.content[decimalIndex + 1:]) or \
                message.content[1:decimalIndex].isdigit() and \
                message.content[decimalIndex + 1:]:
            lost = randrange(2, 5)
            await message.channel.send("Wrong! " + message.author.mention + ". You have lost " + str(lost) + " points.")
            if str(message.author.id) in quizData:
                quizData[str(message.author.id)] -= lost
            else:
                quizData.update({message.author.id: lost * -1})
            fileDump()

    elif typing and message.content.find("!typetest") == -1 and message.content.find("!tt") == -1:
        if message.content == typeString:
            typeEndTimes = timer()
            await message.channel.send("Congratulations," + message.author.mention + ", you typed that string in: " + str(
                round(typeEndTimes - typeStartTime, 2)) + "s for a speed of: " + str(
                round(20 / ((typeEndTimes - typeStartTime) / 60), 2)) + "CPM.")

            CPM = round(20 / ((typeEndTimes - typeStartTime) / 60), 2)
            fileLoad()
            if str(message.author.id) in typetestData:
                if typetestData[str(message.author.id)] < CPM:
                    await message.channel.send(message.author.mention + ", you beat your high score!")
                    typetestData[str(message.author.id)] = CPM
            else:
                typetestData.update({message.author.id: CPM})
            fileDump()

    elif easyTyping and message.content.find("!easytypetest") == -1 and message.content.find("!ett") == -1:
        if message.content == easyTypeString:
            easyTypeEndTime = timer()
            await message.channel.send("Congratulations," + message.author.mention + " you completed the easy type test in: " +
                                       str(round(easyTypeEndTime - easyTypeStartTime, 2)) + "s.")
            fileLoad()
            finalTime = round(easyTypeEndTime - easyTypeStartTime, 2)
            if finalTime < 3:
                await message.channel.send("You copy-pasted that didn't you? As punishment, your high scores will be messed with.")
                if str(message.author.id) in ettData:
                    ettData[str(message.author.id)] = 1000
                else:
                    ettData.update({message.author.id: 1000})
            elif str(message.author.id) in ettData:
                if ettData[str(message.author.id)] > finalTime:
                    await message.channel.send(message.author.mention + ", you beat your high score!")
                    ettData[str(message.author.id)] = finalTime
            else:
                ettData.update({message.author.id: finalTime})
            fileDump()

    else:
        if message.content.find("69420") != -1:
            await message.channel.send('BIG NICE')
        elif message.content.find("420 ") != -1 or message.content.find(" 420") != -1 or message.content == "420":
            await message.channel.send("Blaze it.")
        elif message.content.find("69 ") != -1 or message.content.find(" 69") != -1 or message.content == "69":
            await message.channel.send("Nice")
        elif message.content.lower().find("fuck") != -1 or message.content.lower().find("bitch") != -1 or message.content.lower().find("shit") != -1:
            await message.channel.send(message.author.mention + " WATCH YOUR PROFANITY.")
        elif message.content.lower().find("sad") != -1 or message.content.lower().find("oof") != -1 or message.content.lower().find("yikes") != -1:
            resp = ['Fs in the chat bois', 'F']
            await message.channel.send(random.choice(resp))
        elif (message.content.lower().find("i'm") != -1 or message.content.lower().find(
                "i am") != -1 or message.content.lower().find("im ") != -1) and not message.author.bot:
            data = message.content.split()
            index = 0
            while True:
                if data[index].lower() == "i'm" or data[index].lower() == "am" or data[index].lower() == 'im':
                    break
                index += 1
                if index == 1000:
                    break
            response = ""
            idx = index + 1
            for word in data[index + 1:]:
                if idx == len(data) - 1:
                    response += word
                else:
                    response += word + " "
                    idx += 1
            if index < len(data) and index < 1000:
                await message.channel.send("Hi " + response + ", I'm Dad.")


client.run(TOKEN)
