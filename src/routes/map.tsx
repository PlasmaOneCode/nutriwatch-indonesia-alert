import { createFileRoute } from "@tanstack/react-router";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { RiskMap } from "@/components/dashboard/RiskMap";
import { MapPin } from "lucide-react";

export const Route = createFileRoute("/map")({
  head: () => ({
    meta: [
      { title: "Map View · NutriWatch" },
      { name: "description", content: "Zonasi risiko geospasial dapur umum se-Indonesia." },
    ],
  }),
  component: MapPage,
});

const regions = [
  { name: "DKI Jakarta", critical: 2, warning: 4, safe: 38 },
  { name: "Jawa Barat", critical: 1, warning: 7, safe: 92 },
  { name: "Jawa Timur", critical: 0, warning: 5, safe: 81 },
  { name: "Sumatera Utara", critical: 1, warning: 3, safe: 44 },
  { name: "Sulawesi Selatan", critical: 0, warning: 2, safe: 39 },
  { name: "Kalimantan Barat", critical: 1, warning: 1, safe: 21 },
];

function MapPage() {
  return (
    <DashboardShell>
      <div className="flex items-center gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-navy/10 text-navy ring-1 ring-navy/20">
          <MapPin className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-xl font-bold">Map View</h1>
          <p className="text-xs text-muted-foreground">
            Distribusi geospasial risiko dapur umum berdasarkan skor agregat
          </p>
        </div>
      </div>

      <RiskMap />

      <div className="rounded-2xl border bg-card">
        <div className="p-4 border-b">
          <h3 className="text-sm font-semibold">Ringkasan per Provinsi</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-muted/40 text-xs uppercase tracking-wider text-muted-foreground">
              <tr>
                <th className="text-left px-4 py-2">Provinsi</th>
                <th className="text-right px-4 py-2">Critical</th>
                <th className="text-right px-4 py-2">Warning</th>
                <th className="text-right px-4 py-2">Safe</th>
                <th className="text-right px-4 py-2">Total</th>
              </tr>
            </thead>
            <tbody>
              {regions.map((r) => (
                <tr key={r.name} className="border-t">
                  <td className="px-4 py-2 font-medium">{r.name}</td>
                  <td className="px-4 py-2 text-right text-warn font-semibold">{r.critical}</td>
                  <td className="px-4 py-2 text-right text-gold font-semibold">{r.warning}</td>
                  <td className="px-4 py-2 text-right text-leaf font-semibold">{r.safe}</td>
                  <td className="px-4 py-2 text-right">{r.critical + r.warning + r.safe}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </DashboardShell>
  );
}
