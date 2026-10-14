# FayTermux native bootstrap build specification

This is a reproducibility contract, **not** a claim that a compatible bootstrap has been built.

## Target
- Android application ID: `com.fay.termux`
- Runtime prefix: `/data/data/com.fay.termux/files/usr`
- Home: `/data/data/com.fay.termux/files/home`
- First package variant: `apt-android-7`
- Architectures: `aarch64`, `arm`, `i686`, `x86_64`

## Upstream build dependency

The upstream package sources are at https://github.com/termux/termux-packages .
A dedicated fork is needed to rebuild the bootstrap and all native packages with the FayTermux prefix. Copying upstream ZIPs or replacing path strings inside existing ELF binaries is not a safe substitute.

The package build environment must use a consistent prefix across compiler flags, linker paths, shebangs, pkg-config, scripts, and apt repository metadata. Keep build logs, toolchain version, commit SHA, and checksums. The repository and signed package index must also be usable by `apt`; a custom bootstrap without compatible repositories is not a complete distribution.

## Release artifacts

Publish a manifest in the schema described by `scripts/verify_fay_bootstrap_release.py` with exactly four ABI ZIP files and their SHA-256 hashes. Verify with:

```sh
python3 scripts/verify_fay_bootstrap_release.py /path/to/manifest.json
```

Do not change the app identity or stock bootstrap download URLs until that command passes for actual built archives. Then add a controlled, authenticated source for those archives and validate runtime startup, `pkg update`, `apt install`, Python and Git on real devices.

## Work currently blocked

No FayTermux-native bootstrap archives or compatible apt repository have been built or verified. The app's original `com.termux` identity remains unchanged by design.
