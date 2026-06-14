import { HeartPulse, Wallet, Truck, ChefHat, TrendingUp, TrendingDown } from "lucide-react";

type Metric = {
  label: string;
  score: number; // positive sentiment %
  delta: number;
  icon: typeof HeartPulse;
};

const metrics: Metric[] = [
  { label: "Kesehatan", score: 82, delta: 3.4, icon: HeartPulse },
  { label: "Anggaran", score: 47, delta: -8.1, icon: Wallet },
  { label: "Logistik", score: 64, delta: -2.2, icon: Truck },
  { label: "Kualitas Dapur", score: 71, delta: 1.6, icon: ChefHat },
];

function tone(score: number) {
  if (score >= 75) return { bar: "bg-leaf", text: "text-leaf", chip: "bg-leaf/10 ring-leaf/30" };
  if (score >= 55) return { bar: "bg-gold", text: "text-gold", chip: "bg-gold/10 ring-gold/30" };
  return { bar: "bg-destructive", text: "text-destructive", chip: "bg-destructive/10 ring-destructive/30" };
}

export function SentimentGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      {metrics.map((m) => {
        const t = tone(m.score);
        const Icon = m.icon;
        const up = m.delta >= 0;
        const Trend = up ? TrendingUp : TrendingDown;
        return (
          <div
            key={m.label}
            className="rounded-2xl border bg-card p-5 shadow-sm flex flex-col gap-3"
          >
            <div className="flex items-center justify-between">
              <div className={`grid h-10 w-10 place-items-center rounded-xl ring-1 ${t.chip}`}>
                <Icon className={`h-5 w-5 ${t.text}`} />
              </div>
              <span
                className={`inline-flex items-center gap-1 text-xs font-semibold ${
                  up ? "text-leaf" : "text-destructive"
                }`}
              >
                <Trend className="h-3.5 w-3.5" />
                {up ? "+" : ""}
                {m.delta}%
              </span>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-muted-foreground">
                ABSA · {m.label}
              </p>
              <p className="mt-1 text-3xl font-bold tabular-nums">
                {m.score}
                <span className="text-base font-medium text-muted-foreground">%</span>
              </p>
            </div>
            <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
              <div className={`h-full ${t.bar}`} style={{ width: `${m.score}%` }} />
            </div>
            <p className="text-[11px] text-muted-foreground">
              Skor sentimen positif (IndoBERT)
            </p>
          </div>
        );
      })}
    </div>
  );
}
