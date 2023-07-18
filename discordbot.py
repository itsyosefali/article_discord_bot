import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

article_data = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def save(ctx, category: str, url: str):
    if category not in article_data:
        article_data[category] = []

    article_data[category].append(url)
    await ctx.send(f"Article saved under category '{category}'.")

@bot.command()
async def articles(ctx, category: str):
    if category in article_data:
        articles = article_data[category]
        if len(articles) > 0:
            response = f"Articles in category '{category}':\n"
            for index, article in enumerate(articles, start=1):
                response += f"{index}. {article}\n"
            await ctx.send(response)
        else:
            await ctx.send(f"No articles found in category '{category}'.")
    else:
        await ctx.send(f"No articles found in category '{category}'.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Please try again.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Please provide all the required arguments.")
    else:
        # Handle other exceptions or display a generic error message
        await ctx.send("An error occurred while executing the command.")

bot.run('TOKEN')
