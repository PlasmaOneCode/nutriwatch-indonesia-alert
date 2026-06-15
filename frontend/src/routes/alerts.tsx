import { createFileRoute } from "@tanstack/react-router";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { AlertPanel } from "@/components/dashboard/AlertPanel";
import { Bell, Filter, RefreshCw } from "lucide-react";

export const Route = createFileRoute("/alerts")({
  head: () => ({
    meta: [
      { title: "Live Alerts · NutriWatch" },
      { name: "description", content: "Red-flag notifications real-time dari pipeline streaming." },
    ],
  }),
  component: AlertsPage,
});

const summary = [
  { label: "Critical", value: 3, color: "text-warn", ring: "ring-warn/30", bg: "bg-warn/10" },
  { label: "Warning", value: 11, color: "text-gold", ring: "ring-gold/30", bg: "bg-gold/10" },
  { label: "Info", value: 24, color: "text-navy", ring: "ring-navy/20", bg: "bg-navy/5" },
  { label: "Resolved (24j)", value: 47, color: "text-leaf", ring: "ring-leaf/30", bg: "bg-leaf/10" },
];

function AlertsPage() {
  return (
    <DashboardShell>
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-warn/10 text-warn ring-1 ring-warn/30">
            <Bell className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Live Alerts</h1>
            <p className="text-xs text-muted-foreground">
              Notifikasi anomali dari Spark Streaming &amp; Isolation Forest
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button className="inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 text-xs font-medium hover:bg-muted">
            <Filter className="h-3.5 w-3.5" /> Filter
          </button>
          <button className="inline-flex items-center gap-1.5 rounded-md bg-navy text-navy-foreground px-3 py-1.5 text-xs font-medium hover:bg-navy/90">
            <RefreshCw className="h-3.5 w-3.5" /> Refresh
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {summary.map((s) => (
          <div key={s.label} className={`rounded-2xl border bg-card p-4 ring-1 ${s.ring}`}>
            <div className={`text-xs font-semibold uppercase tracking-wider ${s.color}`}>
              {s.label}
            </div>
            <div className={`mt-2 text-3xl font-bold ${s.color}`}>{s.value}</div>
            <div className={`mt-1 inline-block rounded-full px-2 py-0.5 text-[10px] ${s.bg} ${s.color}`}>
              last 24h
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AlertPanel />
        </div>
        <div className="rounded-2xl border bg-card p-5">
          <h3 className="text-sm font-semibold">Sumber Sinyal</h3>
          <ul className="mt-4 space-y-3 text-sm">
            {[
              { k: "Kafka topic: mbg.complaints", v: "1,247 msg/min" },
              { k: "Kafka topic: mbg.budget-events", v: "84 msg/min" },
              { k: "NiFi flow: kitchen-telemetry", v: "OK" },
              { k: "IsolationForest model", v: "v2.3 · drift 0.4%" },
              { k: "IndoBERT ABSA", v: "v1.1 · F1 0.87" },
            ].map((r) => (
              <li key={r.k} className="flex justify-between gap-3 border-b last:border-0 pb-2">
                <span className="text-muted-foreground">{r.k}</span>
                <span className="font-medium">{r.v}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </DashboardShell>
  );
}
