import { Activity, Bell, Map as MapIcon, FileBarChart, ShieldAlert, Home } from "lucide-react";
import { Link, useRouterState } from "@tanstack/react-router";

const tabs = [
  { to: "/overview", label: "Overview", icon: Activity },
  { to: "/alerts", label: "Live Alerts", icon: Bell },
  { to: "/map", label: "Map View", icon: MapIcon },
  { to: "/reports", label: "Reports", icon: FileBarChart },
] as const;

export function Header() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <header className="bg-navy text-navy-foreground border-b border-gold/30">
      <div className="mx-auto max-w-[1600px] px-6 pt-5 pb-0">
        <div className="flex items-center justify-between gap-4 flex-wrap">
          <Link to="/" className="flex items-center gap-3 min-w-0 group">
            <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-gold/15 ring-1 ring-gold/40 group-hover:bg-gold/25 transition">
              <ShieldAlert className="h-6 w-6 text-gold" />
            </div>
            <div className="min-w-0">
              <h1 className="truncate text-xl sm:text-2xl font-bold tracking-tight">
                <span className="text-gold">NutriWatch</span>
                <span className="text-navy-foreground/80">: Early Warning System MBG</span>
              </h1>
              <p className="text-xs text-navy-foreground/60">Badan Gizi Nasional · Real-time risk monitoring</p>
            </div>
          </Link>
          <div className="flex items-center gap-2 text-xs">
            <Link
              to="/"
              className="inline-flex items-center gap-1.5 rounded-full bg-navy-foreground/5 px-3 py-1 text-navy-foreground/80 ring-1 ring-navy-foreground/15 hover:bg-navy-foreground/10"
            >
              <Home className="h-3 w-3" />
              Beranda
            </Link>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-leaf/15 px-3 py-1 text-leaf ring-1 ring-leaf/40">
              <span className="h-1.5 w-1.5 rounded-full bg-leaf animate-pulse" />
              Stream: LIVE
            </span>
          </div>
        </div>

        <nav className="mt-5 flex gap-1 overflow-x-auto">
          {tabs.map(({ to, label, icon: Icon }) => {
            const isActive = pathname === to;
            return (
              <Link
                key={to}
                to={to}
                className={`group flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap ${
                  isActive
                    ? "border-gold text-gold"
                    : "border-transparent text-navy-foreground/60 hover:text-navy-foreground"
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
