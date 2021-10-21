from private import TOKEN

from discord.ext import commands
from datetime import datetime, time, timedelta
import asyncio

# https://stackoverflow.com/questions/63769685/discord-py-how-to-send-a-message-everyday-at-a-specific-time

bot = commands.Bot(command_prefix="$")
WHEN = time(16, 0, 0)  # 4:00 PM
channel_id = 898169634434461739  # Put your channel id here


async def called_once_a_day():  # Fired every day
    # Make sure your guild cache is ready so the channel can be found via get_channel
    await bot.wait_until_ready()
    # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    channel = bot.get_channel(channel_id)
    await channel.send("C'est l'heure du gouter !!!! (c'est un test)")


async def background_task():
    now = datetime.now()
    print(now)
    # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start
        await asyncio.sleep(seconds)
    while True:
        # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        now = datetime.now()
        target_time = datetime.combine(
            now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        # Sleep until we hit the target time
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # Seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # Sleep until tomorrow and then the loop will start a new iteration
        await asyncio.sleep(seconds)


@bot.command()
async def quand_le_gouter(ctx: commands.Context):
    message = await ctx.send("On fait quand le gouter semaine prochaine ?")
    for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
        await message.add_reaction(emoji)
    await ctx.message.delete()

if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(TOKEN)
