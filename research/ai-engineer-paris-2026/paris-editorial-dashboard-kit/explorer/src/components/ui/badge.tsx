import { cva, type VariantProps } from 'class-variance-authority'
import * as React from 'react'

import { cn } from '../../lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-mono uppercase tracking-wider transition-colors',
  {
    variants: {
      variant: {
        default: 'border-[hsl(var(--border))] bg-[hsl(var(--muted))] text-[hsl(var(--foreground))]',
        accent: 'border-transparent bg-[hsl(var(--primary))]/15 text-orange-300',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}
