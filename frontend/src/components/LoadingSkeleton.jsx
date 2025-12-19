import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function LoadingSkeleton() {
    return (
        <Card className="animate-pulse">
            <CardHeader>
                <div className="h-6 bg-slate-200 rounded-lg w-24"></div>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="h-10 bg-slate-200 rounded-lg w-32"></div>
                <div className="grid grid-cols-2 gap-4">
                    <div className="h-12 bg-slate-200 rounded-lg"></div>
                    <div className="h-12 bg-slate-200 rounded-lg"></div>
                </div>
            </CardContent>
        </Card>
    );
}
