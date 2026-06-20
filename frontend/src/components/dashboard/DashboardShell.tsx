import type { ReactNode } from "react";
import { Header } from "./Header";
import { usePipelineStatus } from "@/lib/api/nutriwatch";

function PipelineHealth() {
  const { data, isLoading, isError } = usePipelineStatus();
  const healthy = !!data?.stream_healthy && !isError;
  const dot = isLoading
    ? "bg-muted-foreground animate-pulse"
    : healthy
      ? "bg-leaf"
      : "bg-destructive";
  const label = isLoading
    ? "Memeriksa pipeline…"
    : isError
      ? "Pipeline tidak terjangkau"
      : healthy
        ? "Stream sehat"
        : "Stream terganggu";
  return (
    <div className="flex items-center justify-center gap-3 text-[11px] text-muted-foreground">
      <span className="inline-flex items-center gap-1.5">
        <span className={`h-2 w-2 rounded-full ${dot}`} />
        <span>{label}</span>
      </span>
      {data && (
        <>
          <span>·</span>
          <span>Spark: {data.spark_throughput_rps.toFixed(2)} rps</span>
          <span>·</span>
          <span>{Array.isArray(data.kafka_topics) ? data.kafka_topics.length : 0} Kafka topics</span>
        </>
      )}
    </div>
  );
}

export function DashboardShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="mx-auto max-w-[1600px] px-6 py-6 space-y-6">
        {children}
        <PipelineHealth />
        <footer className="pt-1 pb-2 text-center text-[11px] text-muted-foreground">
          NutriWatch · Powered by Kafka · NiFi · Spark Streaming · IndoBERT · Elasticsearch
        </footer>
      </main>
    </div>
  );
}
