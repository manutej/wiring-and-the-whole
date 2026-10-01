import { motion, AnimatePresence } from 'motion/react'
import { useEffect, useState } from 'react'

import { Card, CardContent } from './ui/card'

type Stage = { label: string; meta: string }

export function LiveDemo({ stages, accent }: { stages: Stage[]; accent: string }) {
  const [active, setActive] = useState(0)

  useEffect(() => {
    const id = setInterval(() => setActive((a) => (a + 1) % stages.length), 1600)
    return () => clearInterval(id)
  }, [stages.length])

  const stage = stages[active]

  return (
    <Card className="border-[hsl(var(--border))] bg-[hsl(var(--card))]/80">
      <CardContent className="space-y-4 p-6 pt-6">
        <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-[hsl(var(--muted-foreground))]">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full opacity-40" style={{ background: accent }} />
            <span className="relative inline-flex h-2 w-2 rounded-full" style={{ background: accent }} />
          </span>
          Live pipeline
        </div>
        <AnimatePresence mode="wait">
          <motion.div
            key={active}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
            <p className="font-serif text-2xl italic" style={{ color: accent }}>
              {stage.label}
            </p>
            <p className="font-mono text-sm text-[hsl(var(--muted-foreground))]">{stage.meta}</p>
          </motion.div>
        </AnimatePresence>
        <div className="flex gap-1">
          {stages.map((_, i) => (
            <div
              key={i}
              className="h-1 flex-1 rounded-full transition-colors"
              style={{ background: i <= active ? accent : 'hsl(var(--border))' }}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
