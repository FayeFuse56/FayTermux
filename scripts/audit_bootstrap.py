#!/usr/bin/env python3
"""Inspect a Termux bootstrap ZIP before it can be considered for FayTermux.

Usage: python3 scripts/audit_bootstrap.py path/to/bootstrap-aarch64.zip
Never treats a successful audit as proof that all ELF dependencies work.
"""
import argparse
import hashlib
import io
import pathlib
import sys
import zipfile

TARGET_PREFIX = b"/data/data/com.fay.termux/files/usr"
UPSTREAM_PREFIX = b"/data/data/com.termux/files/usr"
CHUNK = 1024 * 1024

def audit(path: pathlib.Path) -> int:
    if not path.is_file():
        print(f"FAIL: missing bootstrap archive: {path}")
        return 1
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            sha.update(block)
    print(f"Archive SHA-256: {sha.hexdigest()}")
    bad = []
    target_hits = 0
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if not names:
                bad.append("empty archive")
            for info in archive.infolist():
                if info.filename.startswith("/") or ".." in pathlib.PurePosixPath(info.filename).parts:
                    bad.append(f"unsafe ZIP path: {info.filename}")
                    continue
                # Stream search with overlap so a prefix crossing chunk boundaries is detected.
                with archive.open(info) as member:
                    tail = b""
                    while True:
                        block = member.read(CHUNK)
                        if not block:
                            break
                        data = tail + block
                        if UPSTREAM_PREFIX in data:
                            bad.append(f"upstream prefix in {info.filename}")
                            break
                        if TARGET_PREFIX in data:
                            target_hits += 1
                        tail = data[-max(len(UPSTREAM_PREFIX), len(TARGET_PREFIX)):]
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        bad.append(f"unreadable archive: {exc}")
    if target_hits == 0:
        bad.append("target FayTermux prefix not found in archive members")
    if bad:
        for error in bad[:30]:
            print(f"FAIL: {error}")
        return 1
    print("PASS: ZIP path/prefix scan; runtime execution and package repository still require testing")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=pathlib.Path)
    args = parser.parse_args()
    sys.exit(audit(args.archive))
