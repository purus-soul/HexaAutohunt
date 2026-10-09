# HexaAutohunt

A personal Telethon client for monitoring encounters in the Telegram game bot
@HeXamonbot. This project is separate from the game bot and does not modify its
code or service.

## Watchlist behavior

While hunting is enabled, an incoming game message that names a Pokémon from
the configured watchlist pauses the automatic hunt loop. Any message containing
the word "shiny" also triggers a pause. The script sends an alert to the logged-in
Telegram account's Saved Messages.

The script does not click encounter buttons, battle, or catch the target. Review
and handle the encounter manually, then send /resume from the same Telegram
account to continue. Send /go to start hunting and /stop to stop the loop.

Detection currently uses message text, not the image attached to a message.
Names that only appear in an image may not be detected.

## Requirements

- Python 3.10 or newer recommended
- A Telegram API ID and API hash from https://my.telegram.org
- Permission to use automation in accordance with the game and Telegram rules

## Setup

1. Create a private local copy of this repository.
2. Install dependencies:

   ```bash
   python -m pip install -r requirement.txt
   ```

3. Copy `.env.example` to a file named `.env`.
4. Fill in your own `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`,
   `TELEGRAM_PHONE_NUMBER`, and `TELEGRAM_GAME_CHAT`. The chat can be a
   numeric ID or a username such as `@HeXamonbot`.
5. Keep `.env` and Telethon session files private. They must never be committed.
6. Run:

   ```bash
   python main.py
   ```

The first run may ask for the Telegram login code and, if enabled, the
two-factor-authentication password. Never share these with anyone.

## Commands

- `/go` — start the hunt loop
- `/resume` — resume after a watchlist or shiny alert
- `/stop` — stop hunting

Send commands from the same logged-in Telegram account, for example in Saved
Messages. Notifications also go to Saved Messages.

## Timing and limitations

`HUNT_INTERVAL_SECONDS` defaults to 10 seconds and should be adjusted only
with regard to game behavior and applicable rules. A command already sent or
being processed when a target appears cannot be recalled; test with care.

## Tests

Run the watchlist matching tests with:

```bash
python -m unittest discover -s tests
```

## Security note

If credentials were ever committed to a public repository, removing them from
the latest file is not enough because they may remain in Git history. Replace
exposed credentials where possible, review active Telegram sessions, and
consider cleaning the repository history before making it public again.
