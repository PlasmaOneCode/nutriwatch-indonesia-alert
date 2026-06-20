import { useEffect, useState } from "react";
import { useIncidents, coordsForRegion } from "@/lib/api/nutriwatch";

function levelFromVictims(v: number): "safe" | "warning" | "critical" {
  if (v >= 100) return "critical";
  if (v >= 30) return "warning";
  return "safe";
}

const colorMap = {
  safe: "var(--leaf)",
  warning: "var(--gold)",
  critical: "var(--warn)",
};

export function RiskMap() {
  const [Comp, setComp] = useState<any>(null);
  const { data, isLoading } = useIncidents(30);

  useEffect(() => {
    Promise.all([import("react-leaflet"), import("leaflet")]).then(([rl]) => {
      setComp(() => rl);
    });
  }, []);

  const markers = (data ?? []).map((inc) => {
    const [lat, lng] = coordsForRegion(inc.region);
    // tiny jitter so overlapping regions don't collapse
    const seed = inc.id.length;
    return {
      ...inc,
      lat: lat + ((seed % 7) - 3) * 0.05,
      lng: lng + ((seed % 5) - 2) * 0.05,
      level: levelFromVictims(inc.victim_count),
    };
  });

  return (
    <div className="rounded-2xl border bg-card text-card-foreground shadow-sm overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b">
        <div>
          <h2 className="text-sm font-semibold">Zonasi Risiko Dapur Umum di Indonesia</h2>
          <p className="text-xs text-muted-foreground">
            {isLoading ? "Memuat insiden…" : `${markers.length} insiden · 30 hari`}
          </p>
        </div>
        <div className="flex items-center gap-3 text-[11px]">
          <Legend color="var(--leaf)" label="Safe" />
          <Legend color="var(--gold)" label="Warning" />
          <Legend color="var(--warn)" label="High Risk" />
        </div>
      </div>
      <div className="h-[440px] w-full bg-secondary/40">
        {Comp ? (
          <Comp.MapContainer
            center={[-2.5, 117]}
            zoom={4.5}
            style={{ height: "100%", width: "100%" }}
            scrollWheelZoom={false}
          >
            <Comp.TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {markers.map((m) => (
              <Comp.CircleMarker
                key={m.id}
                center={[m.lat, m.lng]}
                radius={m.level === "critical" ? 14 : m.level === "warning" ? 10 : 8}
                pathOptions={{
                  color: colorMap[m.level],
                  fillColor: colorMap[m.level],
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >
                <Comp.Popup>
                  <div className="text-xs">
                    <strong>{m.location}</strong>
                    <br />
                    {m.region} · {m.date}
                    <br />
                    Korban: <strong>{m.victim_count}</strong>
                  </div>
                </Comp.Popup>
              </Comp.CircleMarker>
            ))}
          </Comp.MapContainer>
        ) : (
          <div className="grid h-full place-items-center text-xs text-muted-foreground">
            Loading map…
          </div>
        )}
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <span className="h-2.5 w-2.5 rounded-full" style={{ background: color }} />
      <span className="text-muted-foreground">{label}</span>
    </span>
  );
}
