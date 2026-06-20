import { HeartPulse, Utensils, Truck, ShieldCheck } from "lucide-react";
import { useAspects, ASPECT_LABELS, type Aspect } from "@/lib/api/nutriwatch";
import { Skeleton } from "@/components/ui/skeleton";

const ICONS: Record<string, typeof HeartPulse> = {
  rasa_menu: Utensils,
  porsi_kecukupan: HeartPulse,
  distribusi_ketepatan: Truck,
  higienitas_keamanan: ShieldCheck,
};

const ORDER = [
  "rasa_menu",
  "porsi_kecukupan",
  "distribusi_ketepatan",
  "higienitas_keamanan",
];

function tone(negative: number) {
  // higher negative_pct = worse
  if (negative >= 70) return { bar: "bg-destructive", text: "text-destructive", chip: "bg-destructive/10 ring-destructive/30" };
  if (negative >= 45) return { bar: "bg-gold", text: "text-gold", chip: "bg-gold/10 ring-gold/30" };
  return { bar: "bg-leaf", text: "text-leaf", chip: "bg-leaf/10 ring-leaf/30" };
}

export function SentimentGrid() {
  const { data, isLoading, isError } = useAspects(30);

  const byKey = new Map<string, Aspect>();
  (data ?? []).forEach((a) => byKey.set(a.aspect, a));

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      {ORDER.map((key) => {
        const m = byKey.get(key);
        const Icon = ICONS[key] ?? HeartPulse;
        const label = ASPECT_LABELS[key] ?? key;
        const neg = m?.negative_pct ?? 0;
        const t = tone(neg);
        return (
          <div
            key={key}
            className="rounded-2xl border bg-card p-5 shadow-sm flex flex-col gap-3"
          >
            <div className="flex items-center justify-between">
              <div className={`grid h-10 w-10 place-items-center rounded-xl ring-1 ${t.chip}`}>
                <Icon className={`h-5 w-5 ${t.text}`} />
              </div>
              <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
                {m ? `${m.total_mentions.toLocaleString("id-ID")} mentions` : ""}
              </span>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-muted-foreground">
                ABSA · {label}
              </p>
              {isLoading ? (
                <Skeleton className="mt-2 h-9 w-24" />
              ) : (
                <p className="mt-1 text-3xl font-bold tabular-nums">
                  {isError || !m ? "—" : neg.toFixed(1)}
                  <span className="text-base font-medium text-muted-foreground">% neg</span>
                </p>
              )}
            </div>
            <div className="h-1.5 w-full rounded-full bg-muted overflow-hidden">
              <div className={`h-full ${t.bar}`} style={{ width: `${Math.min(100, neg)}%` }} />
            </div>
            <p className="text-[11px] text-muted-foreground">
              Sentimen negatif (IndoBERT · 30 hari)
            </p>
          </div>
        );
      })}
    </div>
  );
}
