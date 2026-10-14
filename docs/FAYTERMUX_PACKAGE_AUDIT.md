# FayTermux independent APK: package and bootstrap audit

Status: **audit only**. Do not install a renamed APK yet.

## Confirmed upstream dependencies

- `app/build.gradle` uses namespace `com.termux` and a manifest placeholder `TERMUX_PACKAGE_NAME = "com.termux"`.
- `termux-shared/src/main/java/com/termux/shared/termux/TermuxConstants.java` documents that `TERMUX_PACKAGE_NAME` must match the app's Android application ID.
- Upstream explicitly states bootstrap binaries embed the app-private prefix path, and require recompilation when the application package name changes.
- `.github/workflows/debug_build.yml` builds the upstream `apt-android-7` and `apt-android-5` variants. Its successful build does not establish that a renamed application can run.
- `app/build.gradle` retrieves official bootstrap archives, which must not be reused unchanged for a different app-private path.

## Proposed application identity

- Android application ID: `com.fay.termux`
- App files: `/data/data/com.fay.termux/files`
- Prefix: `/data/data/com.fay.termux/files/usr`
- Home: `/data/data/com.fay.termux/files/home`
- Keep Java namespaces unchanged initially; Android application ID and Java namespaces serve different purposes.

## Required before applying the rename

1. Fork `termux/termux-packages` and configure package builds for the proposed prefix.
2. Produce reproducible, per-ABI bootstrap archives and publish hashes and build provenance.
3. Update bootstrap download URLs and CI to use only matching FayTermux artifacts.
4. Audit app identity references, manifest placeholders, shared constants, content providers, shortcuts, preferences, and plugin intents.
5. Build an APK on a feature branch and test on a clean emulator before distributing.
6. Validate `sh`, `apt`, `pkg`, DNS, SSL certificates, native executables, and package upgrades.
7. Confirm official Termux and FayTermux can coexist with no shared app-private storage.

## Stop conditions

Do not merge an identity rename if the bootstrap is missing, package paths mismatch, or package manager smoke tests fail.

## Appearance development

Image background support can be developed independently on a separate branch, without changing app identity or native bootstrap paths.
