"""Command loop for JARVIS. Phone control goes through Termux:API commands."""

import json
import shutil
import subprocess


def run(cmd):
    """Run a command and return its output, or None if the tool is missing or fails."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        return None
    return result.stdout if result.returncode == 0 else None


def speak(text):
    """Print the text and say it aloud when text-to-speech is available."""
    print(text)
    run(["termux-tts-speak", text])


def battery():
    out = run(["termux-battery-status"])
    if out is None:
        speak("I can't read the battery. Is Termux:API installed?")
        return
    info = json.loads(out)
    state = "charging" if info.get("status") == "CHARGING" else "not charging"
    speak(f"Battery is at {info.get('percentage')} percent and {state}.")


def torch(on):
    if run(["termux-torch", "on" if on else "off"]) is None:
        speak("I can't reach the torch. Is Termux:API installed?")
    else:
        speak("Torch on." if on else "Torch off.")


HELP = "Commands: battery, torch on, torch off, say <text>, help, exit"


def handle(line):
    """Handle one command. Returns False when it is time to quit."""
    line = line.strip()
    lowered = line.lower()
    if lowered in ("exit", "quit"):
        speak("Goodbye.")
        return False
    if lowered == "battery":
        battery()
    elif lowered == "torch on":
        torch(True)
    elif lowered == "torch off":
        torch(False)
    elif lowered.startswith("say "):
        speak(line[4:])
    elif lowered in ("help", "?"):
        print(HELP)
    elif line:
        print("I don't know that one yet. Type 'help'.")
    return True


def main():
    speak("JARVIS online.")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not handle(line):
            break


if __name__ == "__main__":
    main()
