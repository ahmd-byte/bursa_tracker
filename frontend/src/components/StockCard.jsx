import { motion } from "framer-motion";
import { TrendingUp, TrendingDown } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";

export function StockCard({ stock, onClick }) {
    const { symbol, current_price, threshold_up, threshold_down } = stock;

    // Determine if price is in alert zone
    const isAboveThreshold = current_price >= threshold_up;
    const isBelowThreshold = current_price <= threshold_down;
    const isInAlertZone = isAboveThreshold || isBelowThreshold;

    // Calculate distance from thresholds
    const distanceFromUp = ((current_price - threshold_up) / threshold_up) * 100;
    const distanceFromDown = ((current_price - threshold_down) / threshold_down) * 100;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            whileHover={{ scale: 1.02 }}
            onClick={onClick}
            className="cursor-pointer"
        >
            <Card className={isInAlertZone ? "ring-2 ring-primary" : ""}>
                <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                        <span className="text-xl font-bold">{symbol}</span>
                        {isAboveThreshold && (
                            <TrendingUp className="w-6 h-6 text-green-500" />
                        )}
                        {isBelowThreshold && (
                            <TrendingDown className="w-6 h-6 text-red-500" />
                        )}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    {/* Current Price */}
                    <div>
                        <p className="text-sm text-muted-foreground mb-1">Current Price</p>
                        <p className="text-3xl font-bold text-primary">
                            {formatCurrency(current_price)}
                        </p>
                    </div>

                    {/* Thresholds */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-1">
                            <p className="text-xs text-muted-foreground">Upper Threshold</p>
                            <p className="text-sm font-semibold text-green-600">
                                {formatCurrency(threshold_up)}
                            </p>
                            {current_price >= threshold_up && (
                                <p className="text-xs text-green-500 font-medium">
                                    +{distanceFromUp.toFixed(2)}%
                                </p>
                            )}
                        </div>
                        <div className="space-y-1">
                            <p className="text-xs text-muted-foreground">Lower Threshold</p>
                            <p className="text-sm font-semibold text-red-600">
                                {formatCurrency(threshold_down)}
                            </p>
                            {current_price <= threshold_down && (
                                <p className="text-xs text-red-500 font-medium">
                                    {distanceFromDown.toFixed(2)}%
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Alert Status */}
                    {isInAlertZone && (
                        <div className="pt-2 border-t">
                            <p className="text-xs font-semibold text-primary">
                                🔔 Alert Zone Active
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </motion.div>
    );
}
