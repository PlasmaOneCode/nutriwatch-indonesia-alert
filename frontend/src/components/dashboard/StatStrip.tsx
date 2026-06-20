import { Database, Radar, AlertOctagon, Activity, Clock } from "lucide-react";
import { useStats } from "@/lib/api/nutriwatch";
import { Skeleton } from "@/components/ui/skeleton";

const fmtInt = (n: number) =>
  new Intl.NumberFormat("id-ID", { maximumFractionDigits: 0 }).format(n);

export function StatStrip() {
  const { data, isLoading, isError } = useStats();

  const cards = [
    {
      label: "Teks Diproses",
      value: data ? fmtInt(data.total_texts_processed) : "—",
      icon: Database,
      accent: "text-primary",
    },
    {
      label: "Sinyal Bahaya",
      value: data ? fmtInt(data.total_signals_detected) : "—",
      icon: Radar,
      accent: "text-gold",
    },
    {
      label: "Insiden Tercatat",
      value: data ? fmtInt(data.total_incidents_recorded) : "—",
      icon: AlertOctagon,
      accent: "text-destructive",
    },
    {
      label: "Akurasi Prediksi",
      value: data ? `${data.match_rate_pct.toFixed(1)}%` : "—",
      icon: Activity,
      accent: "text-leaf",
    },
    {
      label: "Avg. Lag (hari)",
      value: data ? data.avg_lag_days.toFixed(1) : "—",
      icon: Clock,
      accent: "text-primary",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
      {cards.map((s) => {
        const Icon = s.icon;
        return (
          <div
            key={s.label}
            className="rounded-2xl border bg-card p-4 shadow-sm flex items-center gap-3"
          >
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-secondary">
              <Icon className={`h-5 w-5 ${s.accent}`} />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                {s.label}
              </p>
              {isLoading ? (
                <Skeleton className="mt-1 h-6 w-20" />
              ) : (
                <p className="text-xl font-bold tabular-nums truncate">
                  {isError ? "—" : s.value}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
