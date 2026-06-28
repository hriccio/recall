# Repository Guidelines

This is a hriccio AI-assisted repository.

## Repository Role

- Own one focused game, visualization, simulation, or static interactive web experience.
- Keep the default runtime static unless a decision explicitly adds backend infrastructure.
- Prefer Vite, TypeScript, and Three.js for 3D or visually rich browser work.
- Deploy static output through GitHub Pages when public hosting is needed.

## Project Structure & Module Organization

- `src/main.ts` is the browser entry point.
- `src/` owns application, rendering, simulation, and UI code.
- `index.html` is the Vite HTML entry.
- `dist/` is generated build output and must not be edited.
- `.github/workflows/deploy-pages.yml` publishes the static build when enabled.

## Build, Test, And Development Commands

- `npm install` installs dependencies.
- `npm run dev` starts the local Vite development server.
- `npm run build` type-checks and creates the production bundle.
- `npm run preview` serves the built bundle for local verification.

## Working Rules

- Keep visual behavior verifiable in the browser.
- Use procedural or explicitly licensed assets by default.
- Avoid adding own infrastructure, monitoring, databases, or server runtimes unless the repository purpose requires them.
- Use `hr capability show mcp-usage` for MCP guidance; default allowed MCPs are `chrome-devtools` and `codex-usage`.
- Preserve durable project decisions in Markdown when scope changes.
