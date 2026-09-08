import discord
from discord.ext import commands
from config import token
from logic import Pokemon
from logic import Wizard
from logic import Fighter
import random

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='!', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Outputs the bot's name to the console

# The '!go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to load Pokémon image.")
    else:
        await ctx.send("You have created a Pokémon.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Both participants must have Pokémon to battle!")
    else:
        await ctx.send("Specify the user you want to attack by mentioning them.")
# Running the bot
bot.run(token)
