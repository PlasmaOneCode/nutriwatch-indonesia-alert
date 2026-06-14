import { createFileRoute } from "@tanstack/react-router";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { FileBarChart, Download, FileText, CalendarDays } from "lucide-react";

export const Route = createFileRoute("/reports")({
  head: () => ({
    meta: [
      { title: "Reports · NutriWatch" },
      { name: "description", content: "Laporan periodik dan ekspor data NutriWatch." },
    ],
  }),
  component: ReportsPage,
});

const reports = [
  {
    title: "Laporan Mingguan Red-Flag",
    desc: "Rekap insiden, anomali anggaran, dan keluhan publik selama 7 hari.",
    period: "10–16 Jun 2026",
    size: "1.4 MB",
  },
  {
    title: "Sentimen Bulanan ABSA",
    desc: "Distribusi sentimen per aspek (Kesehatan, Anggaran, Logistik, Kualitas).",
    period: "Mei 2026",
    size: "820 KB",
  },
  {
    title: "Audit Dapur Umum Berisiko",
    desc: "Daftar dapur dengan skor risiko ≥ 0.7 beserta rekomendasi mitigasi.",
    period: "Q2 2026",
    size: "2.1 MB",
  },
  {
    title: "Kinerja Pipeline Streaming",
    desc: "Throughput Kafka/Spark, lag konsumen, dan SLA model NLP.",
    period: "Mei 2026",
    size: "640 KB",
  },
];

function ReportsPage() {
  return (
    <DashboardShell>
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-gold/15 text-gold ring-1 ring-gold/40">
            <FileBarChart className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Reports</h1>
            <p className="text-xs text-muted-foreground">Laporan periodik &amp; ekspor data</p>
          </div>
        </div>
        <button className="inline-flex items-center gap-1.5 rounded-md bg-navy text-navy-foreground px-3 py-1.5 text-xs font-medium hover:bg-navy/90">
          <CalendarDays className="h-3.5 w-3.5" /> Generate New
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {reports.map((r) => (
          <div
            key={r.title}
            className="rounded-2xl border bg-card p-5 flex flex-col gap-3 hover:shadow-md transition"
          >
            <div className="flex items-start gap-3">
              <div className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-secondary text-navy">
                <FileText className="h-5 w-5" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold">{r.title}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{r.desc}</p>
              </div>
            </div>
            <div className="flex items-center justify-between border-t pt-3 mt-1 text-xs">
              <div className="text-muted-foreground">
                {r.period} · {r.size}
              </div>
              <button className="inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 font-medium hover:bg-muted">
                <Download className="h-3.5 w-3.5" /> Unduh PDF
              </button>
            </div>
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}
