import os
import random
import discord
from discord.ext import commands

# 1. Set up basic intents
intents = discord.Intents.default()
intents.message_content = True

# 2. Configure the bot with your custom prefix
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
  print(f"Bot is online as {bot.user}!")
  print("Ready to roll in Discord.")


@bot.command()
async def roll(ctx):
  """Rolls a random number from the pool, removes it, and shows what's left."""
  global remaining_pool

  if not remaining_pool:
    await ctx.send(
        "🎲 **The pool is completely empty!** Use `!!reset` to start a new"
        " round."
    )
    return

  # Pick a random number from the remaining pool
  chosen = random.choice(remaining_pool)
  remaining_pool.remove(chosen)

  await ctx.send(
      f"🎲 **Rolled:** `{chosen}`\n📊 **Numbers left:**"
      f" `{len(remaining_pool)}/{DEFAULT_TOTAL}`"
  )


@bot.command()
async def remaining(ctx):
  """Shows which numbers are still left in the pool."""
  global remaining_pool

  if not remaining_pool:
    await ctx.send("⚠️ No numbers left in the pool.")
    return

  # Format the list neatly
  numbers_str = ", ".join(str(n) for n in remaining_pool)
  if len(numbers_str) > 1900:  # Prevent hitting Discord message character limits
    numbers_str = (
        f"{len(remaining_pool)} numbers remaining (too long to list all)."
    )

  await ctx.send(
      f"📋 **Remaining Pool ({len(remaining_pool)}):** {numbers_str}"
  )


@bot.command()
async def reset(ctx, count: int = DEFAULT_TOTAL):
  """Resets the pool back to 32 (or a custom number like !!reset 50)."""
  global remaining_pool, DEFAULT_TOTAL

  if count < 1:
    await ctx.send("⚠️ Enter a number greater than 0.")
    return
  if count > 1000:
    await ctx.send("⚠️ Pool capped at 1,000 for performance.")
    return

  DEFAULT_TOTAL = count
  remaining_pool = list(range(1, count + 1))
  await ctx.send(
      f"🔄 **Pool reset!** Now rolling numbers from `1` to `{count}`."
  )


# 4. Run the bot using the token securely stored in Railway variables
bot.run(os.getenv("DISCORD_TOKEN"))
