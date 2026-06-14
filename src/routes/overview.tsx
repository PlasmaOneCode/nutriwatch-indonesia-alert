import { createFileRoute } from "@tanstack/react-router";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { AlertPanel } from "@/components/dashboard/AlertPanel";
import { RiskMap } from "@/components/dashboard/RiskMap";
import { SentimentGrid } from "@/components/dashboard/SentimentGrid";
import { StatStrip } from "@/components/dashboard/StatStrip";

export const Route = createFileRoute("/overview")({
  head: () => ({
    meta: [
      { title: "Overview · NutriWatch" },
      { name: "description", content: "Ringkasan operasional real-time program MBG." },
    ],
  }),
  component: OverviewPage,
});

function OverviewPage() {
  return (
    <DashboardShell>
      <StatStrip />
      <SentimentGrid />
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2">
          <RiskMap />
        </div>
        <div className="xl:col-span-1">
          <AlertPanel />
        </div>
      </div>
    </DashboardShell>
  );
}
