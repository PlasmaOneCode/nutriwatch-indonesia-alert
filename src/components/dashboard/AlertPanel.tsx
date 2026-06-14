import { AlertTriangle, Clock, MessageSquareWarning, TrendingDown } from "lucide-react";

type Alert = {
  id: string;
  level: "critical" | "warning" | "info";
  title: string;
  message: string;
  location: string;
  time: string;
  icon: typeof AlertTriangle;
};

const alerts: Alert[] = [
  {
    id: "a1",
    level: "critical",
    title: "RED FLAG: Risiko Tinggi Keracunan",
    message:
      "Dapur Umum X mengalami Keterlambatan Dana > 14 Hari & terdeteksi 3 keluhan 'makanan berbau asam'.",
    location: "Dapur Umum X · Jakarta Timur",
    time: "baru saja",
    icon: AlertTriangle,
  },
  {
    id: "a2",
    level: "warning",
    title: "Keterlambatan Distribusi",
    message: "Pengiriman bahan baku terlambat 6 jam dari jadwal rutin.",
    location: "Dapur Umum Y · Bandung",
    time: "4 menit lalu",
    icon: Clock,
  },
  {
    id: "a3",
    level: "warning",
    title: "Sentimen Negatif Meningkat",
    message: "ABSA mendeteksi spike keluhan 'Kualitas Dapur' +38% (1 jam).",
    location: "Region Sulawesi",
    time: "12 menit lalu",
    icon: MessageSquareWarning,
  },
  {
    id: "a4",
    level: "info",
    title: "Anomali Anggaran Terdeteksi",
    message: "Isolation Forest menandai pola pencairan tidak biasa.",
    location: "Dapur Umum Z · Surabaya",
    time: "27 menit lalu",
    icon: TrendingDown,
  },
];

const styles: Record<Alert["level"], string> = {
  critical:
    "border-destructive/60 bg-destructive/5 text-destructive ring-destructive/20",
  warning: "border-gold/50 bg-gold/5 text-gold ring-gold/20",
  info: "border-border bg-muted/40 text-foreground ring-border",
};

export function AlertPanel() {
  return (
    <div className="rounded-2xl border bg-card text-card-foreground shadow-sm">
      <div className="flex items-center justify-between p-4 border-b">
        <div>
          <h2 className="text-sm font-semibold">Red-Flag Notification Feed</h2>
          <p className="text-xs text-muted-foreground">Anomali real-time dari Spark Streaming</p>
        </div>
        <span className="text-[10px] font-medium uppercase tracking-wider rounded-full bg-destructive/10 text-destructive px-2 py-1">
          1 critical
        </span>
      </div>
      <ul className="divide-y max-h-[520px] overflow-y-auto">
        {alerts.map((a) => {
          const Icon = a.icon;
          const isCritical = a.level === "critical";
          return (
            <li
              key={a.id}
              className={`p-4 border-l-4 ${
                isCritical
                  ? "border-l-destructive bg-destructive/5"
                  : a.level === "warning"
                    ? "border-l-gold"
                    : "border-l-transparent"
              }`}
            >
              <div className="flex gap-3">
                <div
                  className={`grid h-9 w-9 shrink-0 place-items-center rounded-full ring-1 ${styles[a.level]} ${
                    isCritical ? "animate-pulse-alert" : ""
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
                      {a.title}
                    </h3>
                    <span className="text-[10px] text-muted-foreground shrink-0">{a.time}</span>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                    {a.message}
                  </p>
                  <p className="mt-2 text-[11px] font-medium text-foreground/70">
                    📍 {a.location}
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
