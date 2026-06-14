import { useEffect, useState } from "react";

type Zone = {
  id: string;
  name: string;
  lat: number;
  lng: number;
  level: "safe" | "warning" | "critical";
};

const zones: Zone[] = [
  { id: "z1", name: "Dapur Umum X — Jakarta Timur", lat: -6.225, lng: 106.9, level: "critical" },
  { id: "z2", name: "Dapur Umum Y — Bandung", lat: -6.914, lng: 107.61, level: "warning" },
  { id: "z3", name: "Dapur Umum Z — Surabaya", lat: -7.257, lng: 112.752, level: "warning" },
  { id: "z4", name: "Dapur Medan", lat: 3.595, lng: 98.672, level: "safe" },
  { id: "z5", name: "Dapur Makassar", lat: -5.147, lng: 119.432, level: "safe" },
  { id: "z6", name: "Dapur Denpasar", lat: -8.65, lng: 115.216, level: "safe" },
  { id: "z7", name: "Dapur Palembang", lat: -2.99, lng: 104.756, level: "warning" },
  { id: "z8", name: "Dapur Banjarmasin", lat: -3.32, lng: 114.59, level: "safe" },
  { id: "z9", name: "Dapur Manado", lat: 1.474, lng: 124.842, level: "safe" },
  { id: "z10", name: "Dapur Pontianak", lat: -0.026, lng: 109.342, level: "critical" },
];

const colorMap = {
  safe: "var(--leaf)",
  warning: "var(--gold)",
  critical: "var(--warn)",
};

export function RiskMap() {
  const [Comp, setComp] = useState<any>(null);

  useEffect(() => {
    // react-leaflet relies on window — load on client only
    Promise.all([import("react-leaflet"), import("leaflet")]).then(([rl]) => {
      setComp(() => rl);
    });
  }, []);

  return (
    <div className="rounded-2xl border bg-card text-card-foreground shadow-sm overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b">
        <div>
          <h2 className="text-sm font-semibold">Zonasi Risiko Dapur Umum di Indonesia</h2>
          <p className="text-xs text-muted-foreground">Heatmap geospasial — OpenStreetMap</p>
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
            {zones.map((z) => (
              <Comp.CircleMarker
                key={z.id}
                center={[z.lat, z.lng]}
                radius={z.level === "critical" ? 14 : z.level === "warning" ? 10 : 8}
                pathOptions={{
                  color: colorMap[z.level],
                  fillColor: colorMap[z.level],
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >
                <Comp.Popup>
                  <div className="text-xs">
                    <strong>{z.name}</strong>
                    <br />
                    Status: {z.level.toUpperCase()}
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
