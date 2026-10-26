# JARVIS

A personal, JARVIS-inspired AI assistant for Android, running in Termux.

**Goals**

- Offline first: core features work without internet
- Low cost: no required paid services
- Voice first: speak to it, it speaks back
- Hybrid brain: a small local model for everyday tasks, with an optional online model for hard ones
- Phone control: battery, torch, volume, apps, calls and messages through Termux:API

**Status:** early skeleton. Text commands, spoken replies and voice input work. The AI brain is next (see the roadmap).

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
| `voice` | Switches to voice mode: say the same commands out loud |
| `help` | Lists commands |
| `exit` | Quits |

### Voice mode

Type `voice`. JARVIS listens through your phone's speech recognition (`termux-speech-to-text`, so it uses Google's recogniser and needs the Termux:API microphone permission).

- Say any command above, for example "battery" or "torch on".
- Say "stop listening" to go back to typing, or "exit" to quit.
- After three silent turns in a row it stops listening on its own.

Termux's speech recognition may send audio to Google, so it is not fully offline. An offline recogniser is on the roadmap.

## Project layout

```
jarvis/
  main.py          command loop and the phone-control actions
setup-termux.sh    installs Termux packages and checks Termux:API
.env.example       settings template (copy to .env)
```

## Roadmap

1. ~~Voice input with `termux-speech-to-text`~~ (done)
2. Offline voice input (for example Vosk), so listening works without internet
3. Local brain: run a small model with `llama.cpp` and wire it to the command loop
4. Optional online brain for hard questions, switched on only when you allow it
5. More phone control: volume, open apps, calls, SMS, reminders
6. Wake word and background service

## Privacy

Commands and replies run on your phone. The one exception is voice input: `termux-speech-to-text` uses Android's speech recogniser, which may send audio to Google. Typed commands never leave the phone. Keys, if you add any, go in `.env`, which git ignores.
