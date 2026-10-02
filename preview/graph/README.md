# Graph preview (Vercel)

Small Next.js app for stakeholder-facing **graph-level** views of [wiring-and-the-whole](https://github.com/manutej/wiring-and-the-whole).

## Pages

| Route | Content |
|-------|---------|
| `/` | Overview links |
| `/wiringmap` | Mermaid from `toybank-accounts.v0.json` |
| `/witness` | iframe → `public/witness/index.html` (from `docs/witness/`) |
| `/pipeline` | `make pipeline-io` sequence (Mermaid) |

## Local dev

```bash
cd preview/graph
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Sync data

When the canonical toybank map changes, refresh the bundled copy:

```bash
cp ../../wiringmap/examples/toybank-accounts.v0.json src/lib/data/
cp ../../docs/witness/index.html public/witness/
```

## Deploy (Vercel)

- **Root directory:** `preview/graph`
- **Framework:** Next.js
- **Build:** `npm run build`

Repo-level `vercel.json` at `preview/graph/vercel.json` sets the app root for monorepo imports.
