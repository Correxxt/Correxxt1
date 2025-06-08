import argparse
from pathlib import Path
import sys
from typing import Iterable
from spellchecker import SpellChecker


DEFAULT_DICT = Path("custom_words.txt")


def load_custom_words(path: Path) -> set[str]:
    if path.exists():
        return {w.strip() for w in path.read_text().splitlines() if w.strip()}
    return set()


def save_custom_words(words: Iterable[str], path: Path) -> None:
    path.write_text("\n".join(sorted(words)) + "\n")


def check_text(text: str, dictionary: Path = DEFAULT_DICT) -> None:
    spell = SpellChecker()
    spell.word_frequency.load_words(load_custom_words(dictionary))
    words = text.split()
    misspelled = spell.unknown(words)
    if not misspelled:
        print("No spelling errors detected.")
        return

    for word in misspelled:
        correction = spell.correction(word)
        candidates = ", ".join(spell.candidates(word))
        print(f"{word} -> {correction} (candidates: {candidates})")


def main():
    parser = argparse.ArgumentParser(description="Check spelling of text or files.")
    parser.add_argument("text", nargs="*", help="Text to check. If omitted, reads from stdin or --file.")
    parser.add_argument("-f", "--file", type=argparse.FileType('r'), help="File to read text from.")
    parser.add_argument("--dict", type=Path, default=DEFAULT_DICT, help="Custom dictionary file.")
    parser.add_argument("--add-word", help="Add a word to the custom dictionary and exit.")
    parser.add_argument("--remove-word", help="Remove a word from the custom dictionary and exit.")
    parser.add_argument("--list-words", action="store_true", help="List words in the custom dictionary and exit.")
    args = parser.parse_args()

    if args.add_word:
        words = load_custom_words(args.dict)
        words.add(args.add_word)
        save_custom_words(words, args.dict)
        print(f"Added '{args.add_word}' to {args.dict}")
        return

    if args.remove_word:
        words = load_custom_words(args.dict)
        if args.remove_word in words:
            words.remove(args.remove_word)
            save_custom_words(words, args.dict)
            print(f"Removed '{args.remove_word}' from {args.dict}")
        else:
            print(f"Word '{args.remove_word}' not found in {args.dict}")
        return

    if args.list_words:
        for word in sorted(load_custom_words(args.dict)):
            print(word)
        return

    if args.file:
        content = args.file.read()
    elif args.text:
        content = " ".join(args.text)
    else:
        content = sys.stdin.read()

    check_text(content, args.dict)


if __name__ == "__main__":
    main()
