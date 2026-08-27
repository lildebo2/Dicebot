import random
import discord
from discord.ext import commands

# 1. Setup lightweight intents
intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

# 2. Ultra-low memory configuration
bot = commands.Bot(
    command_prefix="!!",
    intents=intents,
    max_messages=None,
    member_cache_flags=discord.MemberCacheFlags.none(),
    chunk_guilds_at_startup=False,
)

# 3. Game state & default pool size
DEFAULT_TOTAL = 32
remaining_pool = list(range(1, DEFAULT_TOTAL + 1))


@bot.event
async def on_ready():
  print(f"✅ Bot is online as {bot.user.name}!")
  print("Ready to roll in Discord.")


@bot.command()
async def roll(ctx):
  """Picks a random number without repeats and eliminates it."""
  global remaining_pool

  if not remaining_pool:
    await ctx.send(
        "🚨 **All numbers eliminated!** Type `!reset [count]` to restart."
    )
    return

  # O(1) swap-and-pop elimination
  idx = random.randrange(len(remaining_pool))
  picked = remaining_pool[idx]
  remaining_pool[idx] = remaining_pool[-1]
  remaining_pool.pop()

  await ctx.send(
      f"🎲 **Rolled #{picked}!** (Eliminated)\n"
      f"📊 **{len(remaining_pool)}** numbers remaining."
  )


@bot.command()
async def remaining(ctx):
  """Displays all numbers currently remaining in the pool."""
  if not remaining_pool:
    await ctx.send("No numbers left in the pool.")
    return

  sorted_numbers = sorted(remaining_pool)
  numbers_str = ", ".join(str(n) for n in sorted_numbers)

  if len(numbers_str) > 1800:
    await ctx.send(
        f"📋 **Remaining:** {len(remaining_pool)} numbers active "
        f"({sorted_numbers[0]} ... {sorted_numbers[-1]}). Pool is too large to"
        " display completely."
    )
  else:
    await ctx.send(
        f"📋 **Remaining Numbers ({len(remaining_pool)}):**\n`{numbers_str}`"
    )


@bot.command()
async def reset(ctx, count: int = DEFAULT_TOTAL):
  """Resets the pool. Usage: !reset or !reset 50"""
  global remaining_pool

  if count < 1:
    await ctx.send("⚠️ Enter a number greater than 0.")
    return
  if count > 1000:
    await ctx.send("⚠️ Pool capped at 1,000 for performance.")
    return

  remaining_pool = list(range(1, count + 1))
  await ctx.send(f"🔄 **Pool reset to numbers 1 through {count}.**")


@reset.error
async def reset_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("⚠️ Invalid input. Usage: `!reset` or `!reset <number>`")


# Put your Discord Developer Portal Bot Token inside the quotes below
bot.run("MTU0MjM5NTMyNzQ5ODQyNDQ0MA.Gl96Ms.-XVBKAV9nIaIYpKBL7Bj30A5WMXD33PgYSa42k")

