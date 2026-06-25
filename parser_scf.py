import re
import sys
import json
import os

def parse_scf(file_path):
    """Parse SCF binary file, extract all Shift-JIS strings to JSON."""
    print(f"Memproses file: {file_path}...")
    
    if not os.path.isfile(file_path):
        print(f"Error: File tidak ditemukan: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error membaca file: {e}")
        sys.exit(1)

    # Extract all null-terminated Shift-JIS strings longer than 1 char
    strings = []
    i = 0
    current = bytearray()
    while i < len(data):
        b = data[i]
        # Detect Shift-JIS lead bytes (0x81-0x9F, 0xE0-0xFC) or printable ASCII
        if (0x20 <= b <= 0x7E) or (0x81 <= b <= 0x9F) or (0xE0 <= b <= 0xFC):
            current.append(b)
            # If SJIS lead byte, grab trail byte too
            if (0x81 <= b <= 0x9F) or (0xE0 <= b <= 0xFC):
                i += 1
                if i < len(data):
                    current.append(data[i])
        else:
            if len(current) >= 2:
                try:
                    text = current.decode('shift_jis', errors='ignore').strip()
                    if text and not re.match(r'^[\x00-\x1f!#_\[\]=;.\\/:]+$', text):
                        strings.append({"offset": i - len(current), "original": text, "translated": text})
                except Exception:
                    pass
            current = bytearray()
        i += 1

    # Deduplicate while preserving order
    seen = set()
    unique_strings = []
    for entry in strings:
        if entry["original"] not in seen:
            seen.add(entry["original"])
            unique_strings.append(entry)

    print(f"Ditemukan {len(unique_strings)} string unik.")

    # Output JSON next to the input file
    out_path = os.path.splitext(file_path)[0] + "_parsed.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(unique_strings, f, ensure_ascii=False, indent=2)

    print(f"Hasil disimpan ke: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser_scf.py <file.SCF>")
        sys.exit(1)
    
    parse_scf(sys.argv[1])