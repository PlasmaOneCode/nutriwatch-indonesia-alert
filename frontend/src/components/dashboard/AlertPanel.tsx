import { AlertTriangle, MessageSquareWarning } from "lucide-react";
import { useSignals, ASPECT_LABELS } from "@/lib/api/nutriwatch";
import { Skeleton } from "@/components/ui/skeleton";

function levelOf(score: number, isSignal: boolean): "critical" | "warning" | "info" {
  if (isSignal && score > 0.8) return "critical";
  if (isSignal || score > 0.6) return "warning";
  return "info";
}

export function AlertPanel() {
  const { data, isLoading, isError } = useSignals(30);

  const items = (data ?? [])
    .slice()
    .sort((a, b) => b.anomaly_score - a.anomaly_score);

  const criticalCount = items.filter(
    (s) => s.is_signal && s.anomaly_score > 0.8,
  ).length;

  return (
    <div className="rounded-2xl border bg-card text-card-foreground shadow-sm">
      <div className="flex items-center justify-between p-4 border-b">
        <div>
          <h2 className="text-sm font-semibold">Red-Flag Notification Feed</h2>
          <p className="text-xs text-muted-foreground">
            Anomali real-time dari Spark Streaming
          </p>
        </div>
        <span className="text-[10px] font-medium uppercase tracking-wider rounded-full bg-destructive/10 text-destructive px-2 py-1">
          {criticalCount} critical
        </span>
      </div>
      <ul className="divide-y max-h-[520px] overflow-y-auto">
        {isLoading &&
          Array.from({ length: 4 }).map((_, i) => (
            <li key={i} className="p-4">
              <Skeleton className="h-4 w-2/3" />
              <Skeleton className="mt-2 h-3 w-full" />
              <Skeleton className="mt-1 h-3 w-1/3" />
            </li>
          ))}

        {!isLoading && isError && (
          <li className="p-6 text-center text-xs text-muted-foreground">
            Tidak dapat memuat sinyal anomali.
          </li>
        )}

        {!isLoading && !isError && items.length === 0 && (
          <li className="p-6 text-center text-xs text-muted-foreground">
            Tidak ada sinyal pada 30 hari terakhir.
          </li>
        )}

        {items.map((s) => {
          const level = levelOf(s.anomaly_score, s.is_signal);
          const isCritical = level === "critical";
          const Icon = isCritical ? AlertTriangle : MessageSquareWarning;
          const aspectLabel = ASPECT_LABELS[s.dominant_aspect] ?? s.dominant_aspect;
          return (
            <li
              key={s.id}
              className={`p-4 border-l-4 ${
                isCritical
                  ? "border-l-destructive bg-destructive/5"
                  : level === "warning"
                    ? "border-l-gold"
                    : "border-l-transparent"
              }`}
            >
              <div className="flex gap-3">
                <div
                  className={`grid h-9 w-9 shrink-0 place-items-center rounded-full ring-1 ${
                    isCritical
                      ? "border-destructive/60 bg-destructive/5 text-destructive ring-destructive/20 animate-pulse-alert"
                      : level === "warning"
                        ? "border-gold/50 bg-gold/5 text-gold ring-gold/20"
                        : "border-border bg-muted/40 text-foreground ring-border"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <h3
                      className={`text-sm font-semibold truncate ${
                        isCritical ? "text-destructive" : "text-foreground"
                      }`}
                    >
                      {isCritical ? "RED FLAG · " : ""}
                      Anomali {aspectLabel}
                    </h3>
                    <span className="text-[10px] text-muted-foreground shrink-0">
                      {s.window_date}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                    Skor anomali {s.anomaly_score.toFixed(2)} · volume {s.tweet_volume.toLocaleString("id-ID")} ·
                    sentimen negatif {s.negative_ratio.toFixed(1)}%
                  </p>
                  <p className="mt-2 text-[11px] font-medium text-foreground/70">
                    📍 {s.region}
                  </p>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
