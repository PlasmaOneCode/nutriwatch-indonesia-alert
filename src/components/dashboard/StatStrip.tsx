import { Utensils, Users, ShieldCheck, AlertOctagon } from "lucide-react";

const stats = [
  { label: "Dapur Aktif", value: "12,480", icon: Utensils, accent: "text-primary" },
  { label: "Penerima Manfaat", value: "8.3M", icon: Users, accent: "text-primary" },
  { label: "Zona Aman", value: "94.2%", icon: ShieldCheck, accent: "text-leaf" },
  { label: "Red Flags (24j)", value: "17", icon: AlertOctagon, accent: "text-destructive" },
];

export function StatStrip() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((s) => {
        const Icon = s.icon;
        return (
          <div
            key={s.label}
            className="rounded-2xl border bg-card p-4 shadow-sm flex items-center gap-3"
          >
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-secondary">
              <Icon className={`h-5 w-5 ${s.accent}`} />
            </div>
            <div className="min-w-0">
              <p className="text-[11px] uppercase tracking-wider text-muted-foreground">
                {s.label}
              </p>
              <p className="text-xl font-bold tabular-nums truncate">{s.value}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
