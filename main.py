#!/usr/bin/python3

import os
import sys
import argparse
from tqdm import tqdm

CHUNK_SIZE = 10 * 1024 * 1024  # 10MB
KEY = 0xFF

# Precompute the translation table for XOR
TRANSLATION_TABLE = bytes.maketrans(
    bytes(range(256)), bytes([b ^ KEY for b in range(256)])
)


def split_file(filename, save_dir):
    if os.path.exists(save_dir):
        if os.listdir(save_dir):
            print(f"Directory '{save_dir}' is not empty. Use another save_dir name.")
            sys.exit(1)
    else:
        os.makedirs(save_dir)

    total_size = os.path.getsize(filename)

    with open(filename, "rb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Splitting", ncols=80
    ) as pbar:
        index = 1
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            xored = chunk.translate(TRANSLATION_TABLE)
            part_path = os.path.join(save_dir, f"part{index}")
            with open(part_path, "wb") as pf:
                pf.write(xored)
            index += 1
            pbar.update(len(chunk))
    print(f"Split into {index-1} parts in '{save_dir}'.")


def restore_file(filename, save_dir):
    parts = sorted(
        [f for f in os.listdir(save_dir) if f.startswith("part")],
        key=lambda x: int(x.replace("part", "")),
    )
    if not parts:
        print(f"No parts found in '{save_dir}'.")
        sys.exit(1)

    total_size = sum(os.path.getsize(os.path.join(save_dir, part)) for part in parts)

    with open(filename, "wb") as outfile, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Restoring", ncols=80
    ) as pbar:
        for part in parts:
            part_path = os.path.join(save_dir, part)
            with open(part_path, "rb") as pf:
                data = pf.read()
                outfile.write(data.translate(TRANSLATION_TABLE))
                pbar.update(len(data))
    print(f"Restored file '{filename}' from {len(parts)} parts.")


def main():
    parser = argparse.ArgumentParser(
        description="Split and restore files with XOR and progress bar."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Split and XOR a file.")
    split_parser.add_argument("--file", required=True, help="File to split.")
    split_parser.add_argument(
        "--dir", required=True, help="Directory to save parts."
    )

    restore_parser = subparsers.add_parser("restore", help="Restore a file from parts.")
    restore_parser.add_argument(
        "--file", required=True, help="Filename to restore."
    )
    restore_parser.add_argument(
        "--dir", required=True, help="Directory containing parts."
    )

    args = parser.parse_args()

    if args.command == "split":
        split_file(args.file, args.dir)
    elif args.command == "restore":
        restore_file(args.file, args.dir)


if __name__ == "__main__":
    try:
        from tqdm import tqdm
    except ImportError:
        print("tqdm module not found. Install it using 'pip install tqdm'.")
        sys.exit(1)
    main()
