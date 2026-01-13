import { type InputHTMLAttributes, forwardRef } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string
    error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className = '', label, error, id, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label htmlFor={id} className="mb-1.5 block text-sm font-medium text-slate-700">
                        {label}
                    </label>
                )}
                <input
                    id={id}
                    ref={ref}
                    className={`block w-full rounded-md border text-sm shadow-sm transition-colors focus:border-slate-500 focus:ring-slate-500 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500 ${error
                        ? 'border-red-300 placeholder-red-300 focus:border-red-500 focus:ring-red-500'
                        : 'border-slate-300 placeholder-slate-400'
                        } ${className}`}
                    {...props}
                />
                {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
            </div>
        )
    }
)

Input.displayName = 'Input'
