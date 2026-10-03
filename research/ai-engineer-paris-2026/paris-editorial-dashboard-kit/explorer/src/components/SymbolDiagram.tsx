import { motion } from 'motion/react'

import type { Talk } from '../data/talks'

type Props = { talk: Talk }

export function SymbolDiagram({ talk }: Props) {
  const a = talk.accent

  return (
    <div className="overflow-hidden rounded-xl border border-[hsl(var(--border))] bg-black/40 p-4 sm:p-6">
      <p className="mb-4 font-mono text-[10px] uppercase tracking-[0.2em] text-[hsl(var(--muted-foreground))]">
        Symbolic map · {talk.metaphor}
      </p>
      <svg viewBox="0 0 640 280" className="w-full" role="img" aria-label={`Concept diagram for ${talk.title}`}>
        {talk.diagram === 'pr-pipeline' && <PrPipeline a={a} />}
        {talk.diagram === 'review-cliff' && <ReviewCliff a={a} />}
        {talk.diagram === 'factory-loop' && <FactoryLoop a={a} />}
        {talk.diagram === 'build-buy' && <BuildBuy a={a} />}
        {talk.diagram === 'orchestra-pit' && <OrchestraPit a={a} />}
        {talk.diagram === 'dx-radar' && <DxRadar a={a} />}
      </svg>
    </div>
  )
}

function box(x: number, y: number, w: number, h: number, label: string, color: string) {
  return (
    <g key={label}>
      <rect x={x} y={y} width={w} height={h} rx="6" fill={`${color}22`} stroke={color} strokeWidth="1.5" />
      <text x={x + w / 2} y={y + h / 2 + 4} textAnchor="middle" fill="#e5e5e5" fontSize="11" fontFamily="Inter, sans-serif">
        {label}
      </text>
    </g>
  )
}

function PrPipeline({ a }: { a: string }) {
  return (
    <>
      {box(20, 100, 100, 44, 'Agent PR', a)}
      {box(160, 100, 100, 44, 'Auto checks', '#60a5fa')}
      {box(300, 100, 100, 44, 'Review agent', '#a78bfa')}
      {box(440, 100, 100, 44, 'Human tier', '#f472b6')}
      {box(560, 100, 60, 44, 'Merge', '#34d399')}
      {[0, 1, 2, 3].map((i) => (
        <motion.line
          key={i}
          x1={120 + i * 140}
          y1={122}
          x2={150 + i * 140}
          y2={122}
          stroke="#666"
          strokeWidth="2"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
        />
      ))}
    </>
  )
}

function ReviewCliff({ a }: { a: string }) {
  return (
    <>
      <motion.path
        d="M 40 200 L 200 200 L 280 80 L 600 80"
        fill="none"
        stroke={a}
        strokeWidth="2.5"
        initial={{ pathLength: 0 }}
        whileInView={{ pathLength: 1 }}
        viewport={{ once: true }}
      />
      <text x="300" y="65" fill="#fca5a5" fontSize="12" fontFamily="monospace">
        review cliff
      </text>
      <text x="80" y="230" fill="#888" fontSize="10">
        agent output
      </text>
      <text x="480" y="105" fill="#888" fontSize="10">
        human bandwidth
      </text>
    </>
  )
}

function FactoryLoop({ a }: { a: string }) {
  return (
    <>
      <motion.circle cx="320" cy="140" r="90" fill="none" stroke={a} strokeWidth="2" strokeDasharray="6 4" animate={{ rotate: 360 }} transition={{ duration: 20, repeat: Infinity, ease: 'linear' }} style={{ originX: '320px', originY: '140px' }} />
      {box(270, 30, 100, 36, 'Intent', a)}
      {box(500, 120, 100, 36, 'Code', a)}
      {box(270, 210, 100, 36, 'Reflect', a)}
      {box(40, 120, 100, 36, 'Test', a)}
    </>
  )
}

function BuildBuy({ a }: { a: string }) {
  return (
    <>
      {box(80, 60, 200, 160, 'Build in-house', a)}
      {box(360, 60, 200, 160, 'Buy vendor', '#60a5fa')}
      <text x="320" y="250" textAnchor="middle" fill="#888" fontSize="11">
        cost · compliance · time-to-value
      </text>
    </>
  )
}

function OrchestraPit({ a }: { a: string }) {
  return (
    <>
      <circle cx="320" cy="60" r="14" fill={a} />
      <text x="320" y="64" textAnchor="middle" fill="#000" fontSize="8" fontWeight="bold">
        you
      </text>
      {[0, 1, 2, 3, 4].map((i) => (
        <motion.g key={i} initial={{ opacity: 0.3 }} animate={{ opacity: [0.3, 1, 0.3] }} transition={{ duration: 2, repeat: Infinity, delay: i * 0.2 }}>
          <line x1="320" y1="74" x2={120 + i * 100} y2="220" stroke={a} strokeWidth="1.2" />
          <rect x={100 + i * 100} y="220" width="40" height="24" rx="4" fill={`${a}33`} stroke={a} />
        </motion.g>
      ))}
    </>
  )
}

function DxRadar({ a }: { a: string }) {
  const cx = 320
  const cy = 140
  return (
    <>
      {[40, 70, 100].map((r) => (
        <circle key={r} cx={cx} cy={cy} r={r} fill="none" stroke="#333" strokeWidth="1" />
      ))}
      <motion.polygon
        points="320,50 390,100 370,190 270,190 250,100"
        fill={`${a}44`}
        stroke={a}
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ duration: 4, repeat: Infinity }}
        style={{ originX: `${cx}px`, originY: `${cy}px` }}
      />
      <text x="320" y="30" textAnchor="middle" fill="#888" fontSize="10">
        DevEx
      </text>
    </>
  )
}
