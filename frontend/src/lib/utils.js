import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind CSS classes with proper precedence
 */
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

/**
 * Format number as Malaysian Ringgit currency
 */
export function formatCurrency(value) {
    if (value === null || value === undefined || isNaN(value)) return "RM 0.00";
    return new Intl.NumberFormat("en-MY", {
        style: "currency",
        currency: "MYR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);
}

/**
 * Format date to readable string
 */
export function formatDate(dateString) {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-MY", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(date);
}

/**
 * Calculate percentage change
 */
export function calculatePercentageChange(current, previous) {
    if (!previous || previous === 0) return 0;
    return ((current - previous) / previous) * 100;
}

/**
 * Format percentage
 */
export function formatPercentage(value) {
    if (value === null || value === undefined || isNaN(value)) return "0.00%";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${value.toFixed(2)}%`;
}
