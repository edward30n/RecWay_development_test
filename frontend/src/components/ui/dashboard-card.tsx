import * as React from "react"
import { LucideIcon } from "lucide-react"
import { cn } from "@/src/lib/utils"

interface DashboardCardProps {
  title: string
  value: number | string
  icon: LucideIcon
  iconColor?: string
  iconBgColor?: string
  description?: React.ReactNode
  chart?: React.ReactNode
  className?: string
  children?: React.ReactNode
}

export function DashboardCard({
  title,
  value,
  icon: Icon,
  iconColor = "text-blue-600",
  iconBgColor = "bg-blue-100",
  description,
  chart,
  className,
  children,
}: DashboardCardProps) {
  return (
    <div className={cn("bg-white rounded-xl border border-gray-100 p-6 shadow-sm", className)}>
      <div className="flex justify-between items-center mb-4">
        <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", iconBgColor)}>
          <Icon className={cn("h-5 w-5", iconColor)} />
        </div>
        {chart && <div className="w-20 h-10">{chart}</div>}
      </div>
      <div className="flex flex-col">
        <span className="text-sm text-gray-500">{title}</span>
        <span className="text-2xl font-bold">{value}</span>
      </div>
      {description && <div className="mt-2">{description}</div>}
      {children && <div className="mt-2">{children}</div>}
    </div>
  )
}
