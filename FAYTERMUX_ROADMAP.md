# FayTermux development roadmap

FayTermux is a community fork of [Termux](https://github.com/termux/termux-app). This repository is currently an **unmodified Termux application fork** with a development roadmap; do not distribute builds as an independently installable app yet.

## Milestone 0 — Baseline
- [ ] Run upstream debug build workflow and verify APK artifacts.
- [ ] Test the stock APK in a clean Android environment.
- [ ] Record upstream commit, Android versions, supported ABIs, and known issues.

## Milestone 1 — Independent application identity
- [ ] Audit hard-coded package identifiers, authorities, permissions, intents, and plugin integrations.
- [ ] Choose `com.fay.termux` as proposed application ID.
- [ ] Rebuild compatible bootstrap for the new app-private prefix and home paths.
- [ ] Validate package manager, shell, executable loading, storage permissions, and upgrades.
- [ ] Ensure installation alongside official Termux without modifying its files.

**Warning:** Changing only `applicationId` is insufficient. Existing Termux binaries and bootstrap may depend on absolute filesystem paths. Do not ship a renamed APK before this is resolved.

## Milestone 2 — Appearance
- [ ] Photo picker background image, stored with scoped app storage.
- [ ] Background opacity and dimming controls.
- [ ] Theme colors, cursor styling, and typography.
- [ ] Accessibility: readable contrast and reduced motion.
- [ ] Preserve terminal rendering performance.

## Milestone 3 — Productivity
- [ ] Session management improvements.
- [ ] File explorer with explicit filesystem permissions.
- [ ] Command shortcuts and command preview.

## Engineering guardrails
- Maintain upstream copyright notices and GPLv3 obligations.
- Never upload signing keys, tokens, or private user data.
- Build pull requests before merging; retain a known-good branch.
- Keep upstream merge conflicts small by isolating appearance features.
- Prefer verified behavior over feature-count claims.
