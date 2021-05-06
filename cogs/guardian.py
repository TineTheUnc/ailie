#!/usr/bin/env python

import discord
from discord.ext import commands
from helpers.database import Database


class Guardian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="profile",
        brief="View profile.",
        description="View profile of yourself or someone else's.",
        aliases=["prof"],
    )
    async def profile(self, ctx, mention: discord.Member = None):
        # Check if user is initialized first
        db_ailie = Database()
        if not db_ailie.is_initialized(ctx.author.id):
            await ctx.send(
                "Do `ailie;initialize` or `a;initialize` first before anything!"
            )
            db_ailie.disconnect()
            return

        # Check if person mentioned is initialized
        if mention:
            if not db_ailie.is_initialized(mention.id):
                await ctx.send(f"{mention.mention} is not initialized yet!")
                db_ailie.disconnect()
                return

        if mention is None:
            guardian_id = ctx.author.id
            guardian_name = ctx.author.name
            guardian_avatar = ctx.author.avatar_url
        else:
            guardian_id = mention.id
            guardian_name = mention.name
            guardian_avatar = mention.avatar_url

        # Get all information needed for a profile show off
        username, guild_name, position, gems = db_ailie.get_guardian_info(
            guardian_id
        )
        guild_id = db_ailie.get_guild_id_of_member(guardian_id)
        heroes_obtained = db_ailie.hero_inventory(guardian_id)
        equips_obtained = db_ailie.equip_inventory(guardian_id)

        # Set embed baseline
        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(
            name=f"{guardian_name}'s Profile", icon_url=guardian_avatar
        )

        # Username and gems
        embed.add_field(name="Username 📝", value=username)
        embed.add_field(name="Gems 💎", value=f"{gems:,d}")

        # Total unique and epic exclusive
        heroes_equips_count = (
            f"Unique Heroes: {len(heroes_obtained[len(heroes_obtained) - 1])}"
            + "\nEpic Exclusive Equipments: "
            + f"{len(equips_obtained[len(equips_obtained) - 1])}"
        )
        embed.add_field(
            name="Unit Counts 🗡️", value=heroes_equips_count, inline=False
        )

        # Guild details
        guild_detail = (
            f"Guild Name: {guild_name}"
            + f"\nGuild ID: {guild_id}"
            + f"\nPosition: {position}"
        )
        embed.add_field(
            name="Guild Details 🏠",
            value=guild_detail,
            inline=False,
        )

        db_ailie.disconnect()

        await ctx.send(embed=embed)

    @commands.command(
        name="inventory",
        brief="View inventory.",
        description=(
            "Open inventory to check what you have collected so far."
            + "Type can be either `hero` or `equip`. "
            + "Mention is optional as it can be used to view "
            + "others' inventories instead."
        ),
        aliases=["inv", "bag"],
    )
    async def inventory(self, ctx, type, mention: discord.Member = None):
        # Check if user is initialized first
        db_ailie = Database()
        if not db_ailie.is_initialized(ctx.author.id):
            await ctx.send(
                "Do `ailie;initialize` or `a;initialize` first before anything!"
            )
            db_ailie.disconnect()
            return

        # Check if person mentioned is initialized
        if mention:
            if not db_ailie.is_initialized(mention.id):
                await ctx.send(f"{mention.mention} is not initialized yet!")
                db_ailie.disconnect()
                return

        if mention is None:
            guardian_id = ctx.author.id
            guardian_name = ctx.author.name
            guardian_avatar = ctx.author.avatar_url
        else:
            guardian_id = mention.id
            guardian_name = mention.name
            guardian_avatar = mention.avatar_url

        # Determine inventory to check
        if type.lower() in ["heroes", "hero", "h"]:
            inventory = db_ailie.hero_inventory(guardian_id)
            if len(inventory[len(inventory) - 1]) > 1:
                header = "Unique Heroes"
            else:
                header = "Unique Hero"
        elif type.lower() in [
            "equipments",
            "equipment",
            "equips",
            "equip",
            "e",
        ]:
            inventory = db_ailie.equip_inventory(guardian_id)
            if len(inventory[len(inventory) - 1]) > 1:
                header = "Epic Exclusive Equipments"
            else:
                header = "Epic Exclusive Equipment"
        else:
            await ctx.send(
                "There's only inventories for heroes and equipments, "
                + f"<@{ctx.author.id}>."
            )
            db_ailie.disconnect()
            return

        embed = discord.Embed(color=discord.Color.purple())
        embed.set_author(
            name=guardian_name + "'s Inventory",
            icon_url=guardian_avatar,
        )
        if len(inventory[len(inventory) - 1]) == 0:
            data = "None"
        else:
            data = "\n".join(inventory[len(inventory) - 1])

        embed.add_field(
            name=header,
            value=data,
            inline=False,
        )
        await ctx.send(embed=embed)

        db_ailie.disconnect()

    @commands.command(
        name="username",
        brief="Set username.",
        description=(
            "Set username that you use in-game or not. "
            + "This is optional. If you set it, you'll see the "
            + "username you set in some commands."
        ),
        aliases=["name", "ign"],
    )
    async def username(self, ctx, username):
        # Check if user is initialized first
        db_ailie = Database()
        if not db_ailie.is_initialized(ctx.author.id):
            await ctx.send(
                "Do `ailie;initialize` or `a;initialize` first before anything!"
            )
            db_ailie.disconnect()
            return

        db_ailie.set_username(ctx.author.id, username)
        await ctx.send(
            f"Your username is now, {username}. Enjoy, <@{ctx.author.id}>."
        )

        db_ailie.disconnect()

    @commands.command(
        name="initialize",
        brief="Initialize user.",
        description=(
            "This command needs to be issued before most of the other commands "
            + "can be used. Think of it as a registration process."
        ),
        aliases=["init"],
    )
    async def initialize(self, ctx):
        db_ailie = Database()

        if db_ailie.initialize_user(ctx.author.id):
            await ctx.send(
                "You can now use the other commands, "
                + f"<@{ctx.author.id}>. Have fun!"
            )
        else:
            await ctx.send(
                f"You are already initialized, <@{ctx.author.id}>. "
                + "No need to initialize for the second time. Have fun!"
            )


def setup(bot):
    bot.add_cog(Guardian(bot))
