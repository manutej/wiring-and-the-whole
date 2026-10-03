#!/usr/bin/env node
/**
 * Lightweight validator: reads explorer/src/data/talks.ts exports by dynamic import after build is not available.
 * Parses talks.ts as text for slug/videoId uniqueness — run full schema validation in agent with JSON exports if needed.
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const talksPath = path.join(__dirname, '../explorer/src/data/talks.ts')
const src = fs.readFileSync(talksPath, 'utf8')

const slugs = [...src.matchAll(/slug:\s*'([^']+)'/g)].map((m) => m[1])
const videoIds = [...src.matchAll(/videoId:\s*'([^']+)'/g)].map((m) => m[1])

function dupes(arr) {
  const seen = new Set()
  const d = new Set()
  for (const x of arr) {
    if (seen.has(x)) d.add(x)
    seen.add(x)
  }
  return [...d]
}

const ds = dupes(slugs)
const dv = dupes(videoIds)
if (ds.length || dv.length) {
  console.error('Duplicate slugs:', ds)
  console.error('Duplicate videoIds:', dv)
  process.exit(1)
}

console.log(`OK: ${slugs.length} talks, slugs unique, videoIds unique`)
