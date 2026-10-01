import { Link, useLocation } from 'react-router-dom'

import { cn } from '../lib/utils'
import { talks } from '../data/talks'

export function SiteNav() {
  const { pathname } = useLocation()

  return (
    <header className="sticky top-0 z-40 border-b border-[hsl(var(--border))] bg-[hsl(var(--background))]/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-3 px-4 py-3 sm:px-6">
        <Link to="/" className="font-serif text-lg italic tracking-tight text-orange-300">
          Paris 2026
        </Link>
        <span className="hidden text-xs font-mono uppercase tracking-widest text-[hsl(var(--muted-foreground))] sm:inline">
          concept explorer
        </span>
        <nav className="ml-auto flex max-w-full gap-1 overflow-x-auto pb-1 text-xs sm:text-sm">
          {talks.map((t) => (
            <Link
              key={t.slug}
              to={`/talk/${t.slug}`}
              className={cn(
                'whitespace-nowrap rounded-md px-2 py-1 transition-colors',
                pathname === `/talk/${t.slug}`
                  ? 'bg-[hsl(var(--muted))] text-[hsl(var(--foreground))]'
                  : 'text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]',
              )}
            >
              {t.speaker.split(' ')[0]}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  )
}
