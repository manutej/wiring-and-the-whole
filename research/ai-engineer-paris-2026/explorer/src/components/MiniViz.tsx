import { motion } from 'motion/react'

import type { VizKind } from '../data/talks'

type Props = { kind: VizKind; accent: string }

export function MiniViz({ kind, accent }: Props) {
  return (
    <div
      className="relative flex h-[130px] items-center justify-center overflow-hidden rounded-lg p-3"
      style={{ background: 'rgba(0,0,0,0.35)', border: '1px solid hsl(var(--border))' }}
    >
      <svg viewBox="0 0 200 110" className="h-full w-full" aria-hidden>
        {kind === 'deep-module' && <DeepModule accent={accent} />}
        {kind === 'review-gate' && <ReviewGate accent={accent} />}
        {kind === 'eval-loop' && <EvalLoop accent={accent} />}
        {kind === 'factory-line' && <FactoryLine accent={accent} />}
        {kind === 'enterprise-stack' && <EnterpriseStack accent={accent} />}
        {kind === 'orchestra' && <Orchestra accent={accent} />}
        {kind === 'survey-radar' && <SurveyRadar accent={accent} />}
      </svg>
    </div>
  )
}

function DeepModule({ accent }: { accent: string }) {
  return (
    <>
      <motion.rect
        x="40"
        y="25"
        width="120"
        height="60"
        rx="6"
        fill={`${accent}22`}
        stroke={accent}
        strokeWidth="1.2"
        initial={{ opacity: 0.4 }}
        animate={{ opacity: [0.4, 1, 0.4] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
      <rect x="55" y="40" width="90" height="8" rx="2" fill={accent} opacity="0.9" />
      <text x="100" y="75" textAnchor="middle" fill={accent} fontSize="8" fontFamily="monospace">
        public API
      </text>
      <motion.g
        initial={{ opacity: 0 }}
        animate={{ opacity: [0, 1, 0] }}
        transition={{ duration: 2.5, repeat: Infinity, delay: 0.5 }}
      >
        <text x="100" y="58" textAnchor="middle" fill="#888" fontSize="7">
          hidden complexity
        </text>
      </motion.g>
    </>
  )
}

function ReviewGate({ accent }: { accent: string }) {
  return (
    <>
      {[0, 1, 2, 3].map((i) => (
        <motion.circle
          key={i}
          cx={35 + i * 40}
          cy="55"
          r="8"
          fill={`${accent}33`}
          stroke={accent}
          initial={{ x: 0 }}
          animate={{ x: i === 3 ? 0 : [0, 20, 0] }}
          transition={{ duration: 2, repeat: Infinity, delay: i * 0.3 }}
        />
      ))}
      <motion.rect
        x="150"
        y="42"
        width="28"
        height="26"
        rx="4"
        stroke="#f87171"
        fill="#f8717122"
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ duration: 1.2, repeat: Infinity }}
      />
      <text x="164" y="58" textAnchor="middle" fill="#fca5a5" fontSize="7">
        gate
      </text>
    </>
  )
}

function EvalLoop({ accent }: { accent: string }) {
  return (
    <motion.g animate={{ rotate: 360 }} transition={{ duration: 10, repeat: Infinity, ease: 'linear' }} style={{ originX: '100px', originY: '55px' }}>
      <circle cx="100" cy="55" r="32" fill="none" stroke={accent} strokeWidth="2" strokeDasharray="5 4" />
      <text x="100" y="58" textAnchor="middle" fill={accent} fontSize="8">
        eval
      </text>
    </motion.g>
  )
}

function FactoryLine({ accent }: { accent: string }) {
  return (
    <>
      <line x1="20" y1="70" x2="180" y2="70" stroke="#555" strokeWidth="1" />
      {[0, 1, 2, 3].map((i) => (
        <motion.rect
          key={i}
          x={30 + i * 42}
          y="45"
          width="28"
          height="20"
          rx="3"
          fill={`${accent}44`}
          stroke={accent}
          initial={{ y: 45 }}
          animate={{ y: [45, 38, 45] }}
          transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.25 }}
        />
      ))}
    </>
  )
}

function EnterpriseStack({ accent }: { accent: string }) {
  return (
    <>
      {[0, 1, 2].map((i) => (
        <motion.rect
          key={i}
          x={50 + i * 8}
          y={30 + i * 18}
          width={100 - i * 10}
          height="14"
          rx="2"
          fill={`${accent}${20 + i * 10}`}
          stroke={accent}
          initial={{ opacity: 0.5 }}
          animate={{ opacity: 1 }}
          transition={{ delay: i * 0.2 }}
        />
      ))}
    </>
  )
}

function Orchestra({ accent }: { accent: string }) {
  return (
    <>
      {[0, 1, 2, 3].map((i) => (
        <motion.line
          key={i}
          x1="100"
          y1="25"
          x2={40 + i * 40}
          y2="85"
          stroke={accent}
          strokeWidth="1"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1, opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, delay: i * 0.15 }}
        />
      ))}
      <circle cx="100" cy="25" r="6" fill={accent} />
    </>
  )
}

function SurveyRadar({ accent }: { accent: string }) {
  const pts = '100,30 140,50 130,90 70,90 60,50'
  return (
    <>
      <polygon points={pts} fill={`${accent}18`} stroke={accent} strokeWidth="1" />
      <motion.polygon
        points="100,45 125,55 120,80 80,78 72,55"
        fill={`${accent}55`}
        animate={{ opacity: [0.3, 0.8, 0.3] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
    </>
  )
}
