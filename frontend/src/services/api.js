import axios from "axios";

// Base API URL - adjust if backend runs on different port
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});

// API service methods
export const api = {
    /**
     * Health check endpoint
     */
    async getHealth() {
        const response = await apiClient.get("/health");
        return response.data;
    },

    /**
     * Get all monitored stocks with current prices
     */
    async getStocks() {
        const response = await apiClient.get("/stocks");
        return response.data;
    },

    /**
     * Get specific stock details
     */
    async getStock(symbol) {
        const response = await apiClient.get(`/stocks/${symbol}`);
        return response.data;
    },

    /**
     * Get price history
     */
    async getHistory(limit = 100) {
        const response = await apiClient.get("/history", {
            params: { limit },
        });
        return response.data;
    },

    /**
     * Get recent alerts
     */
    async getAlerts() {
        const response = await apiClient.get("/alerts");
        return response.data;
    },

    /**
     * Get all thresholds
     */
    async getThresholds() {
        const response = await apiClient.get("/thresholds");
        return response.data;
    },

    /**
     * Update stock threshold
     */
    async updateThreshold(symbol, thresholdData) {
        const response = await apiClient.put(`/thresholds/${symbol}`, thresholdData);
        return response.data;
    },
};

export default api;
