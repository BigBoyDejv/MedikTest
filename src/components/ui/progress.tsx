import * as React from "react";
import { cn } from "@/lib/utils";

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number;
  indicatorClassName?: string;
}

/**
 * Pomocná funkcia pre farebné odlíšenie podľa úspešnosti:
 * - Pod 60 % -> červená
 * - Do 80 % (60 % – 80 %) -> oranžová
 * - Nad 80 % -> zelená
 */
export function getAccuracyColorClasses(accuracy: number) {
  if (accuracy < 60) {
    return {
      bar: "bg-red-500",
      text: "text-red-600 dark:text-red-400",
      badge: "border-red-500/30 bg-red-50 text-red-700",
    };
  }
  if (accuracy <= 80) {
    return {
      bar: "bg-amber-500",
      text: "text-amber-600 dark:text-amber-400",
      badge: "border-amber-500/30 bg-amber-50 text-amber-700",
    };
  }
  return {
    bar: "bg-emerald-500",
    text: "text-emerald-600 dark:text-emerald-400",
    badge: "border-emerald-500/30 bg-emerald-50 text-emerald-700",
  };
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, indicatorClassName, ...props }, ref) => {
    const clampedValue = Math.max(0, Math.min(100, value));

    return (
      <div
        ref={ref}
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={clampedValue}
        className={cn(
          "relative h-2.5 w-full overflow-hidden rounded-full bg-secondary",
          className
        )}
        {...props}
      >
        <div
          className={cn(
            "h-full w-full flex-1 bg-primary transition-all duration-500 ease-out",
            indicatorClassName
          )}
          style={{ transform: `translateX(-${100 - clampedValue}%)` }}
        />
      </div>
    );
  }
);
Progress.displayName = "Progress";

export { Progress };

