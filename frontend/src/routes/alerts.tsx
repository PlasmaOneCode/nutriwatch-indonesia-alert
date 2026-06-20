import { createFileRoute } from "@tanstack/react-router";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { AlertPanel } from "@/components/dashboard/AlertPanel";
import { Bell, Filter, RefreshCw } from "lucide-react";
import { useSignals, usePipelineStatus } from "@/lib/api/nutriwatch";

export const Route = createFileRoute("/alerts")({
  head: () => ({
    meta: [
      { title: "Live Alerts · NutriWatch" },
      { name: "description", content: "Red-flag notifications real-time dari pipeline streaming." },
    ],
  }),
  component: AlertsPage,
});

function AlertsPage() {
  const { data: signals } = useSignals(30);
  const { data: pipeline } = usePipelineStatus();
  
  const items = signals ?? [];
  const criticalCount = items.filter((s) => s.is_signal && s.anomaly_score > 0.8).length;
  const warningCount = items.filter((s) => s.is_signal && s.anomaly_score <= 0.8).length;
  const infoCount = items.filter((s) => !s.is_signal).length;
  const totalCount = items.length;

  const summary = [
    { label: "Critical", value: criticalCount, color: "text-warn", ring: "ring-warn/30", bg: "bg-warn/10" },
    { label: "Warning", value: warningCount, color: "text-gold", ring: "ring-gold/30", bg: "bg-gold/10" },
    { label: "Info", value: infoCount, color: "text-navy", ring: "ring-navy/20", bg: "bg-navy/5" },
    { label: "Total (30h)", value: totalCount, color: "text-leaf", ring: "ring-leaf/30", bg: "bg-leaf/10" },
  ];

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
              Notifikasi anomali dari Spark Streaming &amp; Elasticsearch
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
              last 30 days
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AlertPanel />
        </div>
        <div className="rounded-2xl border bg-card p-5">
          <h3 className="text-sm font-semibold">Sumber Sinyal (Real-time)</h3>
          <ul className="mt-4 space-y-3 text-sm">
            {[
              { k: "Kafka Stream", v: pipeline?.stream_healthy ? "SEHAT" : "GANGGUAN" },
              { k: "Spark Throughput", v: `${pipeline?.spark_throughput_rps?.toFixed(2) || 0} msg/sec` },
              { k: "Model AI Aktif", v: pipeline?.model_versions?.[0]?.version || "IndoBERT" },
              { k: "Elasticsearch", v: "Connected" },
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
