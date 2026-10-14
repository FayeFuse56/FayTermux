#!/usr/bin/env python3
"""Fail closed when a renamed FayTermux APK would embed upstream bootstrap paths."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
gradle = (root / "app/build.gradle").read_text()
constants = (root / "termux-shared/src/main/java/com/termux/shared/termux/TermuxConstants.java").read_text()

def require(pattern, content, label):
    match = re.search(pattern, content)
    if not match:
        raise RuntimeError(f"Cannot locate {label}; upstream structure may have changed")
    return match.group(1)

placeholder = require(r'manifestPlaceholders\.TERMUX_PACKAGE_NAME\s*=\s*"([^"]+)"', gradle, "manifest package placeholder")
constant = require(r'public static final String TERMUX_PACKAGE_NAME\s*=\s*"([^"]+)"', constants, "shared package constant")
application_ids = re.findall(r'^\s*applicationId\s+["\']([^"\']+)["\']', gradle, re.M)
identity = application_ids[-1] if application_ids else placeholder

print(f"Manifest package: {placeholder}")
print(f"Shared constant: {constant}")
print(f"Application ID: {identity}")

if len({placeholder, constant, identity}) != 1:
    sys.exit("FAIL: Android identity values differ")
if identity != "com.termux":
    sys.exit("BLOCKED: custom application ID requires a separately rebuilt, verified bootstrap; stock bootstrap must not be used")
print("PASS: upstream identity is consistent; this does NOT validate runtime bootstrap or APK installation")
