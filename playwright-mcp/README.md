# Playwright + MCP Quality Engineering Starter

A self-contained Playwright test automation project with the **Playwright MCP server** pre-configured, so AI assistants (Cursor, Claude Desktop, VS Code Copilot, etc.) can drive a real browser to explore apps, generate locators, reproduce bugs, and help maintain this suite.

## What's inside

| Area | Location | Demonstrates |
|---|---|---|
| E2E UI tests | `tests/e2e/` | User flows on TodoMVC and SauceDemo (login, sorting, full checkout) |
| Page Object Model | `pages/` + `fixtures/pom-fixtures.ts` | Page objects injected via custom fixtures, incl. a `loggedInPage` auth fixture |
| API tests | `tests/api/` | Browser-less `request` fixture: GET/POST/PUT, pagination, search, 404s, schema assertions |
| Network mocking | `tests/network/` | `route.fulfill` response mocking, `route.abort` request blocking, request recording |
| Accessibility | `tests/accessibility/` | axe-core WCAG scans via `@axe-core/playwright` |
| Multi-browser | `playwright.config.ts` | Chromium, Firefox, and WebKit projects + a dedicated `api` project |
| CI | `.github/workflows/playwright.yml` | GitHub Actions with HTML report upload |
| MCP integration | `.cursor/mcp.json` | Playwright MCP with `testing`, `network`, `storage`, `devtools` capabilities |

## Getting started

```bash
npm install
npx playwright install --with-deps   # downloads Chromium, Firefox, WebKit
npm test                             # run everything
```

Useful scripts:

```bash
npm run test:chromium   # single browser
npm run test:api        # API tests only (no browser)
npm run test:headed     # watch the browser
npm run test:ui         # Playwright UI mode (interactive)
npm run test:debug      # step through with the Playwright inspector
npm run report          # open the last HTML report
npm run codegen         # record actions into generated test code
```

Failures automatically capture screenshots, videos, and traces (`trace: 'on-first-retry'`). Open a trace with `npm run trace <path-to-trace.zip>`.

## Playwright MCP integration

`.cursor/mcp.json` registers the official [Playwright MCP server](https://github.com/microsoft/playwright-mcp):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--caps=testing,network,storage,devtools"]
    }
  }
}
```

Open this folder as the workspace root in Cursor and the server is picked up automatically (enable it under Settings → MCP). The AI can then:

- navigate pages and read structured accessibility snapshots (no vision model needed);
- generate resilient locators for new page objects (`browser_generate_locator`);
- assert visibility/text/values while exploring (`browser_verify_*`, from the `testing` capability);
- inspect network requests and mock API responses (`network` capability);
- persist login state between sessions (`storage` capability);
- record traces and videos while reproducing bugs (`devtools` capability).

For Claude Desktop, add the same `mcpServers` block to `claude_desktop_config.json`.

> Security note: do not enable `browser_run_code_unsafe` unless the MCP client runs in an isolated, trusted environment — it executes arbitrary JavaScript in the server process.

## Extracting this folder into its own repository

This project lives as a subfolder and has no dependencies on the parent repo. To turn it into a standalone repo:

```bash
# from the parent repo root
cp -r playwright-mcp ~/playwright-mcp-quality-engineering
cd ~/playwright-mcp-quality-engineering
git init -b main
git add .
git commit -m "Initial commit: Playwright + MCP quality engineering starter"
# create an empty repo on GitHub first, then:
git remote add origin git@github.com:<your-user>/playwright-mcp-quality-engineering.git
git push -u origin main
```

(Or use `git subtree split --prefix=playwright-mcp` in the parent repo if you want to preserve history.)

## Test targets

Tests run against public demo apps: [TodoMVC](https://demo.playwright.dev/todomvc/), [SauceDemo](https://www.saucedemo.com/), and [DummyJSON](https://dummyjson.com/). No local server or credentials required.
