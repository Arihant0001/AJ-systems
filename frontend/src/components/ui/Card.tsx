import { type HTMLAttributes, forwardRef } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
    noPadding?: boolean
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
    ({ className = '', noPadding = false, children, ...props }, ref) => {
        return (
            <div
                ref={ref}
                className={`overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md ${className}`}
                {...props}
            >
                <div className={noPadding ? '' : 'p-5'}>{children}</div>
            </div>
        )
    }
)

Card.displayName = 'Card'
