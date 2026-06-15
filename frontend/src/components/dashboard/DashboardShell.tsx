import type { ReactNode } from "react";
import { Header } from "./Header";

export function DashboardShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="mx-auto max-w-[1600px] px-6 py-6 space-y-6">
        {children}
        <footer className="pt-4 pb-2 text-center text-[11px] text-muted-foreground">
          NutriWatch · Powered by Kafka · NiFi · Spark Streaming · IndoBERT · Elasticsearch
        </footer>
      </main>
    </div>
  );
}
