import { motion } from 'motion/react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Radio } from 'lucide-react'

import { talks } from '../data/talks'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'

function TalkCard({ talk, index }: { talk: (typeof talks)[0]; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{ delay: index * 0.06 }}
      whileHover={{ y: -6 }}
    >
      <Link to={`/talk/${talk.slug}`} className="block h-full">
        <Card
          className="group h-full overflow-hidden transition-colors hover:border-orange-500/40"
          style={{ borderTopColor: talk.accent, borderTopWidth: 3 }}
        >
          <CardHeader>
            <Badge variant="accent" className="w-fit">
              {talk.org}
            </Badge>
            <CardTitle className="font-serif text-xl font-normal leading-snug">{talk.title}</CardTitle>
            <CardDescription>
              {talk.speaker} · {talk.durationMin} min · {talk.transcriptWords.toLocaleString()} words captured
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="line-clamp-3 text-sm text-[hsl(var(--muted-foreground))]">{talk.thesis}</p>
            <span className="mt-4 inline-flex items-center gap-1 text-sm text-orange-300 opacity-0 transition-opacity group-hover:opacity-100">
              Explore concept <ArrowUpRight className="h-4 w-4" />
            </span>
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  )
}

export function HubPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 pb-24 pt-10 sm:px-6">
      <section className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-end">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-[hsl(var(--muted-foreground))]">
            AI Engineer · Station F · Sep 2026
          </p>
          <h1
            className="mt-3 font-serif font-normal leading-[1.05] tracking-tight"
            style={{ fontSize: 'clamp(2.5rem, 8vw, 4.5rem)' }}
          >
            Six talks, six <span className="grad-text italic">symbol systems</span>
          </h1>
          <p className="mt-4 max-w-xl text-[hsl(var(--muted-foreground))]" style={{ lineHeight: 1.65 }}>
            An editorial experiment: each Paris session becomes a shadcn-style concept page — animated mini-viz,
            failure modes, and evidence from TubeAlfred transcripts (auto-generated EN captions).
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild>
              <a href="https://www.youtube.com/@aiDotEngineer" target="_blank" rel="noreferrer">
                <Radio className="h-4 w-4" /> Channel
              </a>
            </Button>
            <Button variant="outline" asChild>
              <a href="https://ai.engineer/paris/2026" target="_blank" rel="noreferrer">
                Schedule
              </a>
            </Button>
          </div>
        </div>
        <motion.div
          className="rounded-xl border border-[hsl(var(--border))] bg-[hsl(var(--card))] p-6"
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <p className="font-mono text-xs uppercase tracking-widest text-[hsl(var(--muted-foreground))]">Floor tension</p>
          <ul className="mt-4 space-y-3 text-sm">
            <li>
              <span className="text-orange-300">Factories</span> vs{' '}
              <span className="text-amber-300">orchestras</span> — competing SDLC metaphors
            </li>
            <li>
              <span className="text-rose-300">PR bottleneck</span> — the constraint every talk orbits
            </li>
            <li>
              <span className="text-emerald-300">DX data</span> — 400+ orgs grounding the hype
            </li>
          </ul>
        </motion.div>
      </section>

      <section className="mt-20">
        <h2 className="font-serif text-3xl italic">Navigate the ingest</h2>
        <p className="mt-2 max-w-2xl text-sm text-[hsl(var(--muted-foreground))]">
          Pick a speaker. Each route is a self-contained concept page: hero demo, symbolic diagram, vocabulary with
          teaching animations, and fault lines.
        </p>
        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {talks.map((t, i) => (
            <TalkCard key={t.slug} talk={t} index={i} />
          ))}
        </div>
      </section>
    </main>
  )
}
