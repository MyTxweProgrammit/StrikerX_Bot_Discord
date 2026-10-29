# StrikerX_Bot_Discord

Discord bot for one server. It answers prefix commands, assigns a role when a member joins, creates a private category and text channel for each non-bot member, and opens a temporary voice room and text channel when someone joins the privacy voice channel. `-pdf-to-image` renders one page of an attached PDF as a PNG.

A Flask app listens on port 8000. `GET /` returns `Server is running!`.

## Setup

The bot reads `TOKEN` from the process environment. It does not load a `.env` file.

Windows Command Prompt:

```
set TOKEN=your-discord-bot-token
```

PowerShell:

```
$env:TOKEN = "your-discord-bot-token"
```

`.env.example` only names the variable. Copy it to `.env` for your own notes if you want. Do not commit a real token.

## Run

```
python run.py
```

`python main.py` starts the same entry point. The hosting start command is not recorded in this repo. Confirm it with the original author before removing `main.py`.

## Commands

- `-bye`
- `-hello`
- `-help`
- `-today`
- `-clear`
- `-role`
- `-pdf-to-image`
