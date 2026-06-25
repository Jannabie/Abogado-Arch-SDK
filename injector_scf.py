import sys
import json
import os

def inject_scf(json_path, scf_path):
    """Inject translated strings from JSON back into the SCF binary file."""
    print(f"Injecting: {json_path} -> {scf_path}")

    if not os.path.isfile(json_path):
        print(f"Error: JSON file tidak ditemukan: {json_path}")
        sys.exit(1)
    if not os.path.isfile(scf_path):
        print(f"Error: SCF file tidak ditemukan: {scf_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    with open(scf_path, 'rb') as f:
        data = bytearray(f.read())

    orig_size = len(data)
    replaced = 0
    skipped = 0

    for entry in entries:
        original = entry.get("original", "")
        translated = entry.get("translated", original)

        if original == translated:
            continue  # Skip untranslated strings

        try:
            orig_bytes = original.encode('shift_jis')
            trans_bytes = translated.encode('shift_jis')
        except UnicodeEncodeError as e:
            print(f"  [SKIP] Encoding error untuk '{original}': {e}")
            skipped += 1
            continue

        if len(trans_bytes) > len(orig_bytes):
            # Trim to fit - cannot expand binary size
            trans_bytes = trans_bytes[:len(orig_bytes)]
            print(f"  [TRIM] '{translated}' dipotong agar sesuai ukuran slot.")
        elif len(trans_bytes) < len(orig_bytes):
            # Pad with spaces to maintain binary size
            trans_bytes = trans_bytes.ljust(len(orig_bytes), b'\x20')

        idx = data.find(orig_bytes)
        if idx != -1:
            data[idx:idx+len(orig_bytes)] = trans_bytes
            print(f"  [OK] '{original}' -> '{translated}'")
            replaced += 1
        else:
            print(f"  [NOT FOUND] '{original}' (mungkin sudah diterjemahkan atau berbeda encoding)")
            skipped += 1

    # Write output next to the SCF file with _injected suffix
    out_path = os.path.splitext(scf_path)[0] + "_injected.SCF"
    with open(out_path, 'wb') as f:
        f.write(data)

    new_size = len(data)
    print(f"\nSelesai: {replaced} string diinjeksi, {skipped} dilewati.")
    print(f"Ukuran asli: {orig_size} bytes | Ukuran baru: {new_size} bytes")
    if orig_size != new_size:
        print("PERINGATAN: Ukuran file berubah! Ini dapat merusak game.")
    else:
        print("Ukuran file tetap sama.")
    print(f"Output: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python injector_scf.py <translation.json> <file.SCF>")
        sys.exit(1)

    inject_scf(sys.argv[1], sys.argv[2])