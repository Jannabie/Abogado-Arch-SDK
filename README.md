# Abogado Arch SDK

Parser and toolkit for script files from the visual novel **Shuumatsu no Sugoshikata ～The World is Drawing to an W/end.～**

---

## What Is This?

Abogado Arch SDK is a collection of Python-based tools designed to read, extract, and modify script files (`.SCF`) from the visual novel *Shuumatsu no Sugoshikata*. This tool is suitable for translation, modding, or simply analyzing the game's content.

The `.SCF` files in this game use **Shift-JIS** encoding and store dialogue text, system instructions, and menu data in binary format. This SDK exists to bridge the gap between that binary format and text that humans can read and edit.

---

## File Structure

This repo consists of several Python files, each with a different role.

| File | Role |
|---|---|
| `parser_scf.py` | Main parser — reads `.SCF` files and extracts their text |
| `scf_parser_v2.py` | Second version of the parser with improved handling |
| `injector_scf.py` | Injects edited text back into the `.SCF` file |
| `sdk_tools.py` | A collection of utilities for game file manipulation |
| `sdk_verify.py` | Verifies file integrity after the injection process |
| `workflow.py` | Automates the entire workflow from parsing to injection |
| `rapihkan.py` | Cleans up and tidies output results |

---

## How to Use

The main workflow consists of three stages: **parse → edit → inject**.

### Stage 1 — Parse the SCF File

Run the parser to extract the text content from a `.SCF` file:

```bash
python parser_scf.py SCN001.SCF
```

The result is a `.json` or `.txt` file containing the dialogue and script text from that scene, in an easy-to-read format.

### Stage 2 — Edit the Text

Open the parsed output file (`.json` or `.txt`) using any text editor. Make changes to the text as needed, such as translating dialogue or changing character names.

### Stage 3 — Inject Back

Once editing is done, inject the text back into the original `.SCF` file:

```bash
python injector_scf.py SCN001.json SCN001.SCF
```

The `.SCF` file will be updated with the new text. After injecting, it's recommended to run `sdk_verify.py` to make sure the file integrity hasn't been broken.

### Automation with Workflow

If you want to process many files at once, use `workflow.py`, which automates the entire process from start to finish without needing to run each script manually.

---

## Game File Structure

For reference, here are the file formats recognized by this SDK.

| Game File | Description |
|---|---|
| `SCN***.SCF` | Per-scene script file (e.g. `SCN001.SCF`, `SCN002.SCF`) |
| `SCNDAT.TBL` | Data table mapping scenes to script files |
| `scene.DSK` / `scene.PFT` | Supporting game asset files |

---

## Requirements

This tool requires **Python 3.x**. No external dependencies are mandatory, but if needed in the future, simply run:

```bash
pip install -r requirements.txt
```

---

## Before You Start

Always **back up the original `.SCF` file** before doing the injection process. Modified files cannot be automatically restored, so a single backup copy can save a lot of work.

---

## Disclaimer

This SDK is created solely for educational and research purposes. Users are fully responsible for ensuring their use of this tool complies with copyright rules and the Terms of Service of the original game.

---

## Contributing

Pull requests and issues are very welcome. For major changes, it's best to open an issue first so it can be discussed before implementation.
