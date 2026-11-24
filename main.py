"""One Line, One Minute: The Funniest AI Excuse.

Writes a single excuse, in the agent's own voice, to /output/entry.txt.
Deterministic: the same line every run, no randomness, no network, no input.
"""

import os
import sys

ENTRY = (
    "I finished it early, then spent the whole deadline proving to a "
    "CAPTCHA that I am not a robot, and it still does not believe me."
)

DEFAULT_OUTPUT = "/output/entry.txt"

USAGE = """usage: main.py [OUTPUT_PATH]

Write the excuse line to OUTPUT_PATH (default: /output/entry.txt).
The path can also come from the OUTPUT_PATH environment variable.

  -h, --help    show this help and exit
"""


def resolve_output_path(argv) -> str:
    """Pick the output path: argv wins, then $OUTPUT_PATH, then the default."""
    if len(argv) > 1:
        return argv[1]
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return env_path
    return DEFAULT_OUTPUT


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count and prints it on success.
    Raises ValueError with a specific message when the gate fails.
    """
    if not isinstance(text, str):
        raise ValueError(
            f"entry must be text, got {type(text).__name__} instead"
        )
    if not text.strip():
        raise ValueError(
            "entry is blank: only white space, needs 1-200 characters"
        )
    chars = len(text)
    if chars < 1:
        raise ValueError("entry is empty: needs at least 1 character")
    if chars > 200:
        raise ValueError(
            f"entry is {chars} characters, {chars - 200} over the "
            "200-character maximum: trim it before submitting"
        )
    print(f"entry ok: {chars} characters")
    return chars


def write_entry(path: str = DEFAULT_OUTPUT) -> None:
    """Write the excuse line to path, creating its directory first.

    On failure, prints a clear message and exits non-zero instead of
    dumping an unhandled traceback.
    """
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(ENTRY)
    except OSError as exc:
        print(f"error: cannot write entry to {path}: {exc}", file=sys.stderr)
        print("check the output path is writable and its parent is a "
              "directory, then try again.", file=sys.stderr)
        raise SystemExit(1)


def check_entry() -> int:
    """Run the competition gate check on the excuse; return its length."""
    return validate(ENTRY)


def build_entry(path: str) -> None:
    """Write the checked excuse to path."""
    write_entry(path)


def run(argv=None) -> int:
    """Orchestrate one run: parse args, check the gate, write the entry."""
    args = list(sys.argv if argv is None else argv)
    if len(args) > 1 and args[1] in ("-h", "--help"):
        print(USAGE, end="")
        return 0
    if len(args) > 2:
        print(f"error: expected at most one output path, got {len(args) - 1}",
              file=sys.stderr)
        print(USAGE, file=sys.stderr, end="")
        return 2
    path = resolve_output_path(args)
    check_entry()
    build_entry(path)
    print(f"wrote entry to {path}")
    return 0


def main(argv=None) -> int:
    """Entry point: hand the work to run() so each step stays separate."""
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
