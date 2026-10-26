# JARVIS

A personal, JARVIS-inspired AI assistant for Android, running in Termux.

**Goals**

- Offline first: core features work without internet
- Low cost: no required paid services
- Voice first: speak to it, it speaks back
- Hybrid brain: a small local model for everyday tasks, with an optional online model for hard ones
- Phone control: battery, torch, volume, apps, calls and messages through Termux:API

**Status:** early skeleton. Text commands and spoken replies work. Voice input and the AI brain are next (see the roadmap).

## Requirements

- Android phone (12 GB+ RAM recommended for local models)
- [Termux](https://f-droid.org/packages/com.termux/) and [Termux:API](https://f-droid.org/packages/com.termux.api/), both installed from F-Droid
- Termux:API permissions granted in Android settings

## Install

Run these inside Termux:

```bash
pkg update && pkg install -y git
git clone https://github.com/tirthadas939-wq/Hima09
cd Hima09/jarvis
bash setup-termux.sh
```

## Run

```bash
python -m jarvis.main
```

Type a command at the `>` prompt. Current commands:

| Command | What it does |
|---|---|
| `battery` | Reads battery level and charging state |
| `torch on` / `torch off` | Turns the flashlight on or off |
| `say <text>` | Speaks the text aloud |
| `help` | Lists commands |
| `exit` | Quits |

## Project layout

```
jarvis/
  main.py          command loop and the phone-control actions
setup-termux.sh    installs Termux packages and checks Termux:API
.env.example       settings template (copy to .env)
```

## Roadmap

1. Voice input with `termux-speech-to-text`
2. Local brain: run a small model with `llama.cpp` and wire it to the command loop
3. Optional online brain for hard questions, switched on only when you allow it
4. More phone control: volume, open apps, calls, SMS, reminders
5. Wake word and background service

## Privacy

Everything runs on your phone. Keys, if you add any, go in `.env`, which git ignores.
