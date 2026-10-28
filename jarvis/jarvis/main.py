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
    try:
        info = json.loads(out)
    except json.JSONDecodeError:
        speak("I got an unreadable answer from the battery. Try again.")
        return
    status = info.get("status")
    if status == "CHARGING":
        state = "charging"
    elif status == "FULL":
        state = "fully charged"
    else:
        state = "not charging"
    speak(f"Battery is at {info.get('percentage')} percent and {state}.")


def torch(on):
    if run(["termux-torch", "on" if on else "off"]) is None:
        speak("I can't reach the torch. Is Termux:API installed?")
    else:
        speak("Torch on." if on else "Torch off.")


def listen():
    """Listen once through the phone's speech recognition. Returns the text, or None."""
    out = run(["termux-speech-to-text"])
    if out is None:
        return None
    text = out.strip()
    return text or None


def clean(text):
    """Turn recognised speech into a command: lowercase, no punctuation, no extra spaces."""
    kept = [c if c.isalnum() or c.isspace() else " " for c in text.lower()]
    return " ".join("".join(kept).split())


MAX_SILENT_TURNS = 3
STOP_PHRASES = ("stop listening", "stop voice", "voice off")


def voice_mode():
    """Take spoken commands until told to stop. Returns False if the user asked to quit."""
    speak("Listening. Say stop listening to go back to typing.")
    silent = 0
    while True:
        heard = listen()
        if heard is None:
            silent += 1
            if silent >= MAX_SILENT_TURNS:
                speak("I didn't hear anything, so I stopped listening.")
                return True
            continue
        silent = 0
        command = clean(heard)
        print(f"Heard: {heard}")
        if command in STOP_PHRASES:
            speak("Okay, back to typing.")
            return True
        if command in ("voice", "listen"):
            continue
        if not handle(command):
            return False


HELP = (
    "Commands: battery, torch on, torch off, say <text>, voice, help, exit\n"
    "In voice mode, say the same commands out loud. Say 'stop listening' to leave it."
)


def handle(line):
    """Handle one command. Returns False when it is time to quit."""
    line = line.strip()
    lowered = line.lower()
    if lowered in ("exit", "quit"):
        speak("Goodbye.")
        return False
    if lowered in ("voice", "listen"):
        return voice_mode()
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
