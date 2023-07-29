import discord
from discord.ext import commands
import requests
import random

intents = discord.Intents.default()
intents.typing = False
intents.members = True
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command(name='say')
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command(name='members')
async def members(ctx):
    members = ctx.guild.members

    member_message_count = {}  # Initialize the member_message_count dictionary

    async for message in ctx.channel.history(limit=None):
        for member in members:
            if message.author == member:
                member_name = member.name
                member_message_count[member] = member_message_count.get(member, 0) + 1

    for member, message_count in member_message_count.items():
        await ctx.send(f'{member.name} - Message Count: {message_count}')

@bot.command(name='trivia')
async def trivia(ctx):
    try:
        # Fetch a random trivia question from the Open Trivia Database API
        response = requests.get('https://opentdb.com/api.php?amount=1&type=multiple')
        if response.status_code == 200:
            data = response.json()
            if data['response_code'] == 0 and len(data['results']) > 0:
                question_data = data['results'][0]
                question = question_data['question']
                correct_answer = question_data['correct_answer']
                incorrect_answers = question_data['incorrect_answers']

                # Combine correct and incorrect answers and shuffle them
                all_answers = [correct_answer] + incorrect_answers
                random.shuffle(all_answers)

                # Send the question and answer options to the user
                options = "\n".join(f"{index + 1}. {answer}" for index, answer in enumerate(all_answers))
                await ctx.send(f"**Trivia Question:**\n{question}\n\n**Options:**\n{options}")

                # Define a check function to verify user responses
                def check(author):
                    def inner(message):
                        return message.author == author and message.channel == ctx.channel
                    return inner

                # Wait for user response
                try:
                    user_response = await bot.wait_for('message', check=check(ctx.author), timeout=20.0)
                except asyncio.TimeoutError:
                    await ctx.send("Time's up! The correct answer was: **{}**".format(correct_answer))
                else:
                    user_answer = user_response.content.strip()
                    if user_answer.lower() == correct_answer.lower():
                        await ctx.send(f"Congratulations {ctx.author.mention}! You got it right!")
                    else:
                        await ctx.send(f"Oops, that's not correct {ctx.author.mention}. The correct answer was: **{correct_answer}**")
            else:
                await ctx.send("Sorry, I couldn't fetch a trivia question at the moment. Please try again later.")
        else:
            await ctx.send("Sorry, there was an error fetching the trivia question. Please try again later.")
    except Exception as e:
        await ctx.send("Sorry, something went wrong. Please try again later.")

# Remember to include your bot token and run the bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
bot.run('MTA0MzI0MDEyODM5NjY2NTAwMw.GLTyTr.RSbYSLrO2NDNunuszPVmkro7S3E_RsHjUhdPKs')
