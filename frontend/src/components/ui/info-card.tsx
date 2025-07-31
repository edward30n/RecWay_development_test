import * as React from "react"
import { LucideIcon } from "lucide-react"
import { cn } from "@/src/lib/utils"

interface InfoCardProps {
  title: string
  description: string
  icon: LucideIcon
  iconColor?: string
  iconBgColor?: string
  action?: React.ReactNode
  className?: string
  children?: React.ReactNode
}

export function InfoCard({
  title,
  description,
  icon: Icon,
  iconColor = "text-blue-600",
  iconBgColor = "bg-blue-100",
  action,
  className,
  children,
}: InfoCardProps) {
  return (
    <div className={cn("flex items-start p-4 rounded-lg border border-gray-100 hover:shadow-sm transition-shadow", className)}>
      <div className={cn("shrink-0 mr-4 rounded-lg p-2", iconBgColor)}>
        <Icon className={cn("h-5 w-5", iconColor)} />
      </div>
      <div className="flex-1">
        <h3 className="font-medium text-gray-900">{title}</h3>
        <p className="mt-1 text-sm text-gray-500">{description}</p>
        {action && <div>{action}</div>}
        {children}
      </div>
    </div>
  )
}
