#!/usr/bin/env python

import os
from helpers.minimal_discord_help import Help
from dotenv import load_dotenv
from discord.ext import commands

if __name__ == "__main__":
    # Get secrets
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    # Bot setup
    bot = commands.Bot(
        command_prefix=["ailie;", "a;"],
        description="Guardian's collector.",
        help_command=Help(),
    )

    # Load extensions
    extensions = ["cogs.info", "cogs.summon", "cogs.guild", "cogs.misc"]

    for extension in extensions:
        bot.load_extension(extension)

    # Run bot
    bot.run(TOKEN)
