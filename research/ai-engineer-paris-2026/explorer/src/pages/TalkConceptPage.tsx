import { motion } from 'motion/react'
import { Link, Navigate, useParams } from 'react-router-dom'
import { ExternalLink, ChevronLeft } from 'lucide-react'

import { getTalk } from '../data/talks'
import { LiveDemo } from '../components/LiveDemo'
import { MiniViz } from '../components/MiniViz'
import { SymbolDiagram } from '../components/SymbolDiagram'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'

export function TalkConceptPage() {
  const { slug } = useParams()
  const talk = slug ? getTalk(slug) : undefined

  if (!talk) {
    return <Navigate to="/" replace />
  }

  return (
    <main className="mx-auto max-w-6xl px-4 pb-24 pt-8 sm:px-6">
      <Link
        to="/"
        className="inline-flex items-center gap-1 text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]"
      >
        <ChevronLeft className="h-4 w-4" /> All talks
      </Link>

      <section className="mt-6 grid gap-10 lg:grid-cols-2 lg:items-start">
        <div>
          <Badge className="mb-3">{talk.metaphor}</Badge>
          <h1
            className="font-serif font-normal leading-tight"
            style={{ fontSize: 'clamp(2rem, 6vw, 3.25rem)' }}
          >
            {talk.title}
          </h1>
          <p className="mt-2 text-[hsl(var(--muted-foreground))]">
            {talk.speaker} · {talk.org}
          </p>
          <p className="mt-6 text-lg" style={{ lineHeight: 1.6 }}>
            {talk.thesis}
          </p>
          <Button className="mt-6" variant="secondary" asChild>
            <a href={`https://www.youtube.com/watch?v=${talk.videoId}`} target="_blank" rel="noreferrer">
              Watch on YouTube <ExternalLink className="h-4 w-4" />
            </a>
          </Button>
        </div>
        <LiveDemo stages={talk.demoStages} accent={talk.accent} />
      </section>

      <section className="mt-20 border-t border-[hsl(var(--border))] pt-16">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[hsl(var(--muted-foreground))]">Bearings</p>
        <div className="mt-6 grid gap-8 sm:grid-cols-3">
          {talk.stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
            >
              <p className="font-serif tabular-nums" style={{ fontSize: 'clamp(2rem, 5vw, 3rem)', color: talk.accent }}>
                {s.value}
              </p>
              <p className="mt-2 text-sm text-[hsl(var(--muted-foreground))]">{s.label}</p>
              {s.cite ? <p className="mt-1 font-mono text-[10px] text-[hsl(var(--muted-foreground))]">{s.cite}</p> : null}
            </motion.div>
          ))}
        </div>
      </section>

      <section className="mt-20">
        <h2 className="font-serif text-2xl italic">Symbolic map</h2>
        <div className="mt-6">
          <SymbolDiagram talk={talk} />
        </div>
      </section>

      <section className="mt-20">
        <h2 className="font-serif text-2xl italic">Vocabulary</h2>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {talk.vocab.map((v) => (
            <Card key={v.term}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">{v.term}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <MiniViz kind={v.viz} accent={talk.accent} />
                <p className="text-sm text-[hsl(var(--muted-foreground))]">{v.def}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mt-20">
        <Tabs defaultValue="symbols">
          <TabsList>
            <TabsTrigger value="symbols">Symbols explained</TabsTrigger>
            <TabsTrigger value="faults">Failure modes</TabsTrigger>
            <TabsTrigger value="evidence">Evidence</TabsTrigger>
          </TabsList>
          <TabsContent value="symbols">
            <div className="grid gap-4 sm:grid-cols-2">
              {talk.symbols.map((s) => (
                <Card key={s.term}>
                  <CardContent className="p-5">
                    <p className="font-medium" style={{ color: talk.accent }}>
                      {s.term}
                    </p>
                    <p className="mt-2 text-sm text-[hsl(var(--muted-foreground))]">{s.meaning}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="faults">
            <div className="space-y-3">
              {talk.failureModes.map((f) => (
                <Card key={f.title} className="border-red-500/20">
                  <CardContent className="p-5">
                    <p className="font-medium text-red-300">{f.title}</p>
                    <p className="mt-2 text-sm text-[hsl(var(--muted-foreground))]">{f.body}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="evidence">
            <Card>
              <CardContent className="space-y-3 p-6 text-sm text-[hsl(var(--muted-foreground))]">
                <p>
                  <strong className="text-[hsl(var(--foreground))]">Transcript:</strong> {talk.transcriptWords.toLocaleString()}{' '}
                  words, English auto-generated captions via TubeAlfred.
                </p>
                <p>
                  <strong className="text-[hsl(var(--foreground))]">Opening hook (abridged):</strong> {talk.hook}
                </p>
                <p className="font-mono text-xs">Video ID: {talk.videoId}</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </section>
    </main>
  )
}
