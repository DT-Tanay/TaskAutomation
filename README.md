# TaskAutomation

** Python Programming **

One menu-driven script with all three automation ideas from the brief:

| Option | Automation | Modules |
|---|---|---|
| 1 | Move all `.jpg` files from a folder into a new folder | `os`, `shutil` |
| 2 | Extract all email addresses from a `.txt` file and save them to another file | `re` |
| 3 | Scrape the title of a webpage and save it | `requests` |

## Setup & run
```bash
pip install -r requirements.txt
python task_automation.py
```
Press **Enter** at any prompt to accept the default shown in `[brackets]`.

## Try it
- **Option 2:** use the included `sample_input.txt` -> creates `emails_found.txt` (duplicates removed).
- **Option 1:** create a folder named `photos` with a few `.jpg` files, then run it. Files are moved to `jpg_images/` and nothing is overwritten.
- **Option 3:** default URL is `https://example.com` -> creates `page_title.txt`.

## Notes
- `.jpg`, `.JPG` and `.jpeg` are all matched.
- Name clashes are handled (`photo.jpg` -> `photo_1.jpg`).
- Errors (missing folder, bad URL, no internet) show a friendly message instead of crashing.
