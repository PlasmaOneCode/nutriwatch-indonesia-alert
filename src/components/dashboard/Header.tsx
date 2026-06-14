import { Activity, Bell, Map as MapIcon, FileBarChart, ShieldAlert } from "lucide-react";

const tabs = [
  { id: "overview", label: "Overview", icon: Activity },
  { id: "alerts", label: "Live Alerts", icon: Bell },
  { id: "map", label: "Map View", icon: MapIcon },
  { id: "reports", label: "Reports", icon: FileBarChart },
];

export function Header({ active, onChange }: { active: string; onChange: (id: string) => void }) {
  return (
    <header className="bg-navy text-navy-foreground border-b border-gold/30">
      <div className="mx-auto max-w-[1600px] px-6 pt-5 pb-0">
        <div className="flex items-center justify-between gap-4 flex-wrap">
          <div className="flex items-center gap-3 min-w-0">
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-gold/15 ring-1 ring-gold/40">
              <ShieldAlert className="h-6 w-6 text-gold" />
            </div>
            <div className="min-w-0">
              <h1 className="truncate text-xl sm:text-2xl font-bold tracking-tight">
                <span className="text-gold">NutriWatch</span>
                <span className="text-navy-foreground/80">: Early Warning System MBG</span>
              </h1>
              <p className="text-xs text-navy-foreground/60">Badan Gizi Nasional · Real-time risk monitoring</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-leaf/15 px-3 py-1 text-leaf ring-1 ring-leaf/40">
              <span className="h-1.5 w-1.5 rounded-full bg-leaf animate-pulse" />
              Stream: LIVE
            </span>
            <span className="hidden sm:inline text-navy-foreground/60">
              Kafka · Spark · ES
            </span>
          </div>
        </div>

        <nav className="mt-5 flex gap-1 overflow-x-auto">
          {tabs.map(({ id, label, icon: Icon }) => {
            const isActive = active === id;
            return (
              <button
                key={id}
                onClick={() => onChange(id)}
                className={`group flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap ${
                  isActive
                    ? "border-gold text-gold"
                    : "border-transparent text-navy-foreground/60 hover:text-navy-foreground"
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
