"""
CodeAlpha Python Programming Internship
Task 3: Task Automation with Python Scripts

The task asks for ONE automation. This script includes all three ideas from
the brief in a single menu-driven tool:

  1. Move all .jpg files from a folder into a new folder.
  2. Extract all email addresses from a .txt file and save them to another file.
  3. Scrape the title of a fixed webpage and save it.

Concepts used: os, shutil, re, requests, file handling.

Install the only third-party dependency with:  pip install requests
"""

import os
import re
import shutil
from html.parser import HTMLParser

try:
    import requests
except ImportError:  # Options 1 and 2 still work without requests.
    requests = None


# --------------------------------------------------------------------------- #
# Automation 1: move .jpg files into a new folder
# --------------------------------------------------------------------------- #
def move_jpg_files(source_folder, destination_folder):
    """
    Move every .jpg / .jpeg file (any letter case) from source_folder into
    destination_folder, creating the destination if needed.
    Returns the list of file names that were moved.
    """
    if not os.path.isdir(source_folder):
        raise FileNotFoundError(f"Source folder not found: {source_folder}")

    os.makedirs(destination_folder, exist_ok=True)
    moved = []

    for name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, name)

        if not os.path.isfile(source_path):
            continue
        if not name.lower().endswith((".jpg", ".jpeg")):
            continue

        target_path = os.path.join(destination_folder, name)

        # Never overwrite: add a number if the name is already taken.
        base, extension = os.path.splitext(name)
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")
            counter += 1

        shutil.move(source_path, target_path)
        moved.append(name)

    return moved


# --------------------------------------------------------------------------- #
# Automation 2: extract email addresses from a text file
# --------------------------------------------------------------------------- #
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


def extract_emails(input_file, output_file):
    """
    Find all email addresses in input_file and write the unique ones
    (one per line, in order of first appearance) to output_file.
    Returns the list of unique emails.
    """
    with open(input_file, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    found = EMAIL_PATTERN.findall(text)

    # dict.fromkeys removes duplicates while keeping the original order.
    # Emails are case-insensitive, so compare them in lowercase.
    unique_emails = list(dict.fromkeys(email.lower() for email in found))

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(unique_emails))
        if unique_emails:
            file.write("\n")

    return unique_emails


# --------------------------------------------------------------------------- #
# Automation 3: scrape the title of a webpage
# --------------------------------------------------------------------------- #
class _TitleParser(HTMLParser):
    """Tiny HTML parser that captures the text inside the <title> tag."""

    def __init__(self):
        super().__init__()
        self._inside_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._inside_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data):
        if self._inside_title:
            self.title += data


def get_page_title(html):
    """Return the <title> text of an HTML string ('' if there is none)."""
    parser = _TitleParser()
    parser.feed(html)
    return " ".join(parser.title.split())  # collapse extra whitespace/newlines


def scrape_title(url, output_file):
    """Download the page at url, extract its title and save it to output_file."""
    if requests is None:
        raise RuntimeError("The 'requests' library is missing. Run: pip install requests")

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"The server returned an error: {error}") from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError("Could not reach the page. Check the URL and your "
                           "internet connection.") from error

    title = get_page_title(response.text)
    if not title:
        raise ValueError("No <title> tag was found on that page.")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"URL: {url}\nTitle: {title}\n")

    return title


# --------------------------------------------------------------------------- #
# Menu (user interface)
# --------------------------------------------------------------------------- #
def ask(prompt, default):
    """Ask for input, falling back to a default when the user presses Enter."""
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def run_move_jpg():
    source = ask("Source folder", "photos")
    destination = ask("Destination folder", "jpg_images")
    moved = move_jpg_files(source, destination)
    if moved:
        print(f"Moved {len(moved)} file(s) to '{destination}':")
        for name in moved:
            print(f"  - {name}")
    else:
        print("No .jpg files were found.")


def run_extract_emails():
    input_file = ask("Input .txt file", "sample_input.txt")
    output_file = ask("Output file", "emails_found.txt")
    emails = extract_emails(input_file, output_file)
    print(f"Found {len(emails)} unique email address(es). Saved to '{output_file}'.")
    for email in emails:
        print(f"  - {email}")


def run_scrape_title():
    url = ask("Webpage URL", "https://example.com")
    output_file = ask("Output file", "page_title.txt")
    title = scrape_title(url, output_file)
    print(f"Page title: {title}")
    print(f"Saved to '{output_file}'.")


def main():
    actions = {
        "1": ("Move all .jpg files to a new folder", run_move_jpg),
        "2": ("Extract email addresses from a .txt file", run_extract_emails),
        "3": ("Scrape the title of a webpage", run_scrape_title),
    }

    while True:
        print("\n" + "=" * 46)
        print("        PYTHON TASK AUTOMATION TOOL")
        print("=" * 46)
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  4. Exit")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break
        if choice not in actions:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")
            continue

        try:
            actions[choice][1]()
        except (OSError, ValueError, RuntimeError) as error:
            print(f"Error: {error}")
        except Exception as error:  # e.g. network errors from requests
            print(f"Something went wrong: {error}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed. Goodbye!")
