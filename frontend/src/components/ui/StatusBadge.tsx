interface StatusBadgeProps {
    status: 'given' | 'reversed' | 'none'
    count?: number
}

export function StatusBadge({ status, count }: StatusBadgeProps) {
    if (status === 'given') {
        return (
            <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-green-500" />
                Given {count !== undefined && count > 1 ? `x${count}` : ''}
            </span>
        )
    }

    if (status === 'reversed') {
        return (
            <span className="inline-flex items-center rounded-full bg-orange-100 px-2.5 py-0.5 text-xs font-medium text-orange-800">
                <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-orange-500" />
                Undo {count !== undefined && count > 0 ? `(-${count})` : ''}
            </span>
        )
    }

    return (
        <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600">
            <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-slate-400" />
            Not Given
        </span>
    )
}
