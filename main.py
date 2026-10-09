import asyncio

from telethon import TelegramClient, events

from config import api_id, api_hash, phone_number, chat, hunt_interval_seconds
from constants import START_COMMAND, STOP_COMMAND, RESUME_COMMAND, HUNT_COMMAND
from utils.helper import find_watchlist_match, build_notification


bot = TelegramClient("session", api_id, api_hash)

hunting_enabled = False
paused = False
hunt_task = None
state_lock = asyncio.Lock()


async def hunt_loop():
    """Send /hunt periodically while enabled and not paused."""
    global hunting_enabled

    try:
        while hunting_enabled:
            if not paused:
                try:
                    await bot.send_message(chat, HUNT_COMMAND)
                except Exception as exc:
                    print(f"Could not send hunt command: {exc}")

            await asyncio.sleep(hunt_interval_seconds)
    except asyncio.CancelledError:
        raise
    finally:
        hunting_enabled = False


async def start_hunting():
    global hunting_enabled, paused, hunt_task

    async with state_lock:
        if hunt_task is not None and not hunt_task.done():
            print("Hunting is already running." if not paused else
                  "Hunting is paused. Send /resume first.")
            return

        paused = False
        hunting_enabled = True
        hunt_task = asyncio.create_task(hunt_loop())

    print("Hunting started.")


async def stop_hunting():
    global hunting_enabled, paused, hunt_task

    async with state_lock:
        hunting_enabled = False
        paused = False
        task = hunt_task
        hunt_task = None
        if task is not None and not task.done():
            task.cancel()

    if task is not None and not task.done():
        try:
            await task
        except asyncio.CancelledError:
            pass

    print("Hunting stopped.")


@bot.on(events.NewMessage(outgoing=True, pattern=r"^/go(?:@\w+)?$"))
async def on_start(event):
    await start_hunting()


@bot.on(events.NewMessage(outgoing=True, pattern=r"^/stop(?:@\w+)?$"))
async def on_stop(event):
    await stop_hunting()


@bot.on(events.NewMessage(outgoing=True, pattern=r"^/resume(?:@\w+)?$"))
async def on_resume(event):
    global paused

    async with state_lock:
        if not hunting_enabled:
            print("Hunting is stopped. Send /go to start.")
            return
        if not paused:
            print("Hunting is not paused.")
            return
        paused = False

    print("Watchlist pause cleared. Hunting will resume.")


@bot.on(events.NewMessage(chats=chat, incoming=True))
async def on_game_message(event):
    global paused

    text = event.raw_text or ""
    name, is_shiny = find_watchlist_match(text)
    if name is None:
        return

    async with state_lock:
        if not hunting_enabled or paused:
            return
        paused = True

    notification = build_notification(name, is_shiny, text)
    try:
        # "me" is Telegram Saved Messages for this logged-in account.
        await bot.send_message("me", notification)
        print(f"Paused for watchlist match: {name}")
    except Exception as exc:
        # Keep hunting paused even if sending the notification fails.
        print(f"PAUSED for {name}, but notification failed: {exc}")
        print(notification)


async def main():
    await bot.start(phone=phone_number)
    print("Connected to Telegram.")
    print("Send /go to start, /resume to resume, or /stop to stop.")
    try:
        await bot.run_until_disconnected()
    finally:
        await stop_hunting()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting.")
