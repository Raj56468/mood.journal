import json
import os
import sys
from datetime import datetime
from textblob import TextBlob

JOURNAL_FILE = "mood_journal.json"

def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def save_entry(entry):
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

def view_entries():
    if not os.path.exists(JOURNAL_FILE):
        print("No journal entries found.")
        return

    with open(JOURNAL_FILE, "r") as f:
        data = json.load(f)

    if not data:
        print("No journal entries found.")
        return

    for i, entry in enumerate(data, 1):
        print(f"Entry {i}:")
        print(f"Date: {entry['date']}")
        print(f"Mood: {entry['mood']}")
        print(f"Text: {entry['text']}")
        print("-" * 40)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--view":
        view_entries()
        return

    print("Write your journal entry (type 'exit' to quit):")
    while True:
        text = input("> ")
        if text.lower() == "exit":
            break
        mood = analyze_mood(text)
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
            "mood": mood
        }
        save_entry(entry)
        print(f"Entry saved! Detected mood: {mood}")

if __name__ == "__main__":
    main()
