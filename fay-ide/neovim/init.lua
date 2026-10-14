-- FayTermux IDE: optional Neovim starter config.
-- Install Neovim, clangd and plugins separately. Requires Neovim 0.12+ for vim.pack.
vim.pack.add({
  { src = "https://github.com/neovim/nvim-lspconfig" },
  { src = "https://github.com/hrsh7th/nvim-cmp" },
  { src = "https://github.com/hrsh7th/cmp-nvim-lsp" },
  { src = "https://github.com/hrsh7th/cmp-buffer" },
  { src = "https://github.com/L3MON4D3/LuaSnip" },
  { src = "https://github.com/onsails/lspkind.nvim" },
})

for _, group in ipairs({ "Pmenu", "PmenuSbar", "NormalFloat", "FloatBorder" }) do
  vim.api.nvim_set_hl(0, group, { bg = "NONE" })
end
vim.api.nvim_set_hl(0, "PmenuSel", { bg = "#2a2e3f" })
vim.api.nvim_set_hl(0, "PmenuThumb", { bg = "#45475a" })

local cmp = require("cmp")
local lspkind = require("lspkind")
cmp.setup({
  snippet = {
    expand = function(args) require("luasnip").lsp_expand(args.body) end,
  },
  mapping = cmp.mapping.preset.insert({
    ["<C-Space>"] = cmp.mapping.complete(),
    ["<CR>"] = cmp.mapping.confirm({ select = true }),
    ["<Tab>"] = cmp.mapping.select_next_item(),
    ["<S-Tab>"] = cmp.mapping.select_prev_item(),
  }),
  sources = cmp.config.sources({
    { name = "nvim_lsp" },
    { name = "buffer" },
  }),
  formatting = {
    format = lspkind.cmp_format({
      mode = "symbol",
      maxwidth = 50,
      ellipsis_char = "...",
    }),
  },
})

vim.lsp.config("clangd", {
  cmd = { "clangd", "--background-index", "--clang-tidy" },
  capabilities = require("cmp_nvim_lsp").default_capabilities(),
  filetypes = { "c", "cpp", "objc", "objcpp", "cuda", "proto" },
  root_markers = { "compile_commands.json", "compile_flags.txt", ".clangd", ".git" },
})
vim.lsp.enable("clangd")
