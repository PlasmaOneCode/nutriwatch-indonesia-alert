import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { AlertPanel } from "@/components/dashboard/AlertPanel";
import { RiskMap } from "@/components/dashboard/RiskMap";
import { SentimentGrid } from "@/components/dashboard/SentimentGrid";
import { StatStrip } from "@/components/dashboard/StatStrip";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "NutriWatch — Early Warning System MBG" },
      {
        name: "description",
        content:
          "Sistem peringatan dini berbasis Big Data untuk program Makan Bergizi Gratis (MBG) Badan Gizi Nasional.",
      },
      { property: "og:title", content: "NutriWatch — Early Warning System MBG" },
      {
        property: "og:description",
        content:
          "Monitoring real-time: red-flag alerts, geospatial risk heatmap, dan ABSA sentiment untuk dapur umum se-Indonesia.",
      },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  const [tab, setTab] = useState("overview");

  return (
    <div className="min-h-screen bg-background">
      <Header active={tab} onChange={setTab} />

      <main className="mx-auto max-w-[1600px] px-6 py-6 space-y-6">
        <StatStrip />
        <SentimentGrid />

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <RiskMap />
          </div>
          <div className="xl:col-span-1">
            <AlertPanel />
          </div>
        </div>

        <footer className="pt-4 pb-2 text-center text-[11px] text-muted-foreground">
          NutriWatch · Powered by Kafka · NiFi · Spark Streaming · IndoBERT · Elasticsearch
        </footer>
      </main>
    </div>
  );
}
