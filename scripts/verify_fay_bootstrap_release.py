#!/usr/bin/env python3
"""Validate a FayTermux bootstrap release manifest and its local ZIP archives.

Manifest schema:
{
  "package_id": "com.fay.termux",
  "prefix": "/data/data/com.fay.termux/files/usr",
  "variant": "apt-android-7",
  "archives": {
    "aarch64": {"path": "/local/bootstrap-aarch64.zip", "sha256": "<64 hex>"},
    "arm": {"path": "/local/bootstrap-arm.zip", "sha256": "<64 hex>"},
    "i686": {"path": "/local/bootstrap-i686.zip", "sha256": "<64 hex>"},
    "x86_64": {"path": "/local/bootstrap-x86_64.zip", "sha256": "<64 hex>"}
  }
}
Paths are local build artifacts; this tool does not download or execute untrusted archives.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ABIS = {"aarch64", "arm", "i686", "x86_64"}
PACKAGE = "com.fay.termux"
PREFIX = f"/data/data/{PACKAGE}/files/usr"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=pathlib.Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text())
        if data.get("package_id") != PACKAGE or data.get("prefix") != PREFIX:
            raise ValueError("package_id/prefix mismatch")
        if data.get("variant") != "apt-android-7":
            raise ValueError("only apt-android-7 is currently targeted")
        archives = data.get("archives")
        if not isinstance(archives, dict) or set(archives) != ABIS:
            raise ValueError("expected exactly four ABI archives")
        for abi, spec in sorted(archives.items()):
            expected = spec["sha256"]
            if not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise ValueError(f"{abi}: invalid SHA-256")
            path = pathlib.Path(spec["path"])
            if not path.is_absolute():
                path = args.manifest.parent / path
            if not path.is_file():
                raise ValueError(f"{abi}: missing archive {path}")
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            if digest.hexdigest() != expected:
                raise ValueError(f"{abi}: SHA-256 mismatch")
            audit = pathlib.Path(__file__).with_name("audit_bootstrap.py")
            result = subprocess.run([sys.executable, str(audit), str(path)], check=False)
            if result.returncode:
                raise ValueError(f"{abi}: prefix/ZIP audit failed")
            print(f"PASS {abi}: {expected}")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: all ABI artifacts verified. Runtime/package manager testing still required.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
