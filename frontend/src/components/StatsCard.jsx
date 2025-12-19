import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export function StatsCard({ title, value, icon: Icon, trend, className }) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
        >
            <Card className={cn("overflow-hidden", className)}>
                <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                        <div className="space-y-2">
                            <p className="text-sm font-medium text-muted-foreground">
                                {title}
                            </p>
                            <p className="text-3xl font-bold">{value}</p>
                            {trend && (
                                <p className={cn(
                                    "text-xs font-medium",
                                    trend.isPositive ? "text-green-600" : "text-red-600"
                                )}>
                                    {trend.text}
                                </p>
                            )}
                        </div>
                        {Icon && (
                            <div className="p-4 bg-gradient-to-br from-primary/20 to-primary/10 rounded-2xl">
                                <Icon className="w-8 h-8 text-primary" />
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
}
