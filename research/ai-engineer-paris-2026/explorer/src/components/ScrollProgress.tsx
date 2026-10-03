import { motion, useScroll, useTransform } from 'motion/react'

export function ScrollProgress() {
  const { scrollYProgress } = useScroll()
  const width = useTransform(scrollYProgress, [0, 1], ['0%', '100%'])

  return (
    <div className="pointer-events-none fixed inset-x-0 top-0 z-50 h-0.5 bg-[hsl(var(--border))]">
      <motion.div className="h-full origin-left bg-gradient-to-r from-orange-500 via-amber-400 to-rose-400" style={{ width }} />
    </div>
  )
}
