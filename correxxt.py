import argparse
import sys
from spellchecker import SpellChecker


def check_text(text: str) -> None:
    spell = SpellChecker()
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
    args = parser.parse_args()

    if args.file:
        content = args.file.read()
    elif args.text:
        content = " ".join(args.text)
    else:
        content = sys.stdin.read()

    check_text(content)


if __name__ == "__main__":
    main()
