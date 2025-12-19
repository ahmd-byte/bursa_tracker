import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import toast from "react-hot-toast";
import { RefreshCw, TrendingUp, Bell, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StockCard } from "@/components/StockCard";
import { StatsCard } from "@/components/StatsCard";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { api } from "@/services/api";

export function Dashboard() {
    const [stocks, setStocks] = useState([]);
    const [alerts, setAlerts] = useState({});
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    // Fetch stocks data
    const fetchStocks = async (showToast = false) => {
        try {
            if (showToast) {
                setRefreshing(true);
                toast.loading("Fetching latest stock prices...", { id: "fetch-stocks" });
            }

            const stocksData = await api.getStocks();
            const alertsData = await api.getAlerts();

            setStocks(stocksData);
            setAlerts(alertsData.alerts || {});

            if (showToast) {
                toast.success("Stock prices updated!", { id: "fetch-stocks" });
            }
        } catch (error) {
            console.error("Error fetching stocks:", error);
            if (showToast) {
                toast.error("Failed to fetch stock data. Please try again.", {
                    id: "fetch-stocks",
                });
            }
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    // Initial load
    useEffect(() => {
        fetchStocks();

        // Auto-refresh every 5 minutes
        const interval = setInterval(() => {
            fetchStocks();
        }, 5 * 60 * 1000);

        return () => clearInterval(interval);
    }, []);

    // Calculate stats
    const totalStocks = stocks.length;
    const activeAlerts = stocks.filter(
        (stock) =>
            stock.current_price >= stock.threshold_up ||
            stock.current_price <= stock.threshold_down
    ).length;

    const handleRefresh = () => {
        fetchStocks(true);
    };

    const handleStockClick = (stock) => {
        toast.success(`Viewing details for ${stock.symbol}`, {
            icon: "📊",
        });
    };

    return (
        <div className="min-h-screen p-6 md:p-8 lg:p-12">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="text-center space-y-4"
                >
                    <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                        Bursa Stock Tracker
                    </h1>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                        Monitor Malaysian stock prices in real-time with intelligent alerts
                    </p>
                </motion.div>

                {/* Stats Cards */}
                {!loading && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <StatsCard
                            title="Total Stocks"
                            value={totalStocks}
                            icon={Activity}
                        />
                        <StatsCard
                            title="Active Alerts"
                            value={activeAlerts}
                            icon={Bell}
                            trend={
                                activeAlerts > 0
                                    ? { text: "Attention needed", isPositive: false }
                                    : { text: "All clear", isPositive: true }
                            }
                        />
                        <StatsCard
                            title="Market Status"
                            value="Live"
                            icon={TrendingUp}
                            trend={{ text: "Real-time data", isPositive: true }}
                        />
                    </div>
                )}

                {/* Actions */}
                <div className="flex justify-center">
                    <Button
                        onClick={handleRefresh}
                        disabled={refreshing}
                        size="lg"
                        className="gap-2"
                    >
                        <RefreshCw className={`w-5 h-5 ${refreshing ? "animate-spin" : ""}`} />
                        {refreshing ? "Refreshing..." : "Refresh Prices"}
                    </Button>
                </div>

                {/* Stocks Grid */}
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[1, 2, 3].map((i) => (
                            <LoadingSkeleton key={i} />
                        ))}
                    </div>
                ) : stocks.length > 0 ? (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                    >
                        {stocks.map((stock, index) => (
                            <motion.div
                                key={stock.symbol}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.4, delay: index * 0.1 }}
                            >
                                <StockCard
                                    stock={stock}
                                    onClick={() => handleStockClick(stock)}
                                />
                            </motion.div>
                        ))}
                    </motion.div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-20"
                    >
                        <div className="glass rounded-3xl p-12 max-w-md mx-auto">
                            <Activity className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
                            <h3 className="text-2xl font-bold mb-2">No Stocks Found</h3>
                            <p className="text-muted-foreground">
                                Add stocks to your watchlist to start monitoring
                            </p>
                        </div>
                    </motion.div>
                )}

                {/* Footer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: 0.4 }}
                    className="text-center text-sm text-muted-foreground pt-8"
                >
                    <p>Made with ❤️ for Bursa Malaysia traders</p>
                    <p className="mt-2">
                        Data updates every 5 minutes • Last updated: {new Date().toLocaleTimeString()}
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
