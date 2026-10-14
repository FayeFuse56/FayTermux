# FayTermux IDE — initial foundation

This directory holds optional editor integrations; it is not an Android IDE implementation yet.

## Neovim starter

The `neovim/init.lua` file is based on the user-supplied custom-background snippet, with corrected Lua syntax and completion/LSP configuration.

Prerequisites:
- Neovim 0.12+ with `vim.pack.add`
- `clangd` for C/C++ language support
- Internet access for first plugin installation

Install manually **after** a working FayTermux bootstrap is available:

```sh
pkg install neovim clangd
mkdir -p ~/.config/nvim
cp init.lua ~/.config/nvim/init.lua
nvim
```

The copy command assumes the working directory contains the downloaded `init.lua` file. Existing `~/.config/nvim/init.lua` should be backed up first.

## Planned Android integration (not implemented)

1. Stable native bootstrap and package compatibility.
2. File explorer and file-open intents.
3. Editor surface and project workspace.
4. Git integration and opt-in AI assistant (no embedded API keys).
5. Mobile touch keyboard shortcuts, performance and security tests.

The appearance work is tracked separately on this branch. Neither the native bootstrap nor the Android IDE has been validated on a device.
