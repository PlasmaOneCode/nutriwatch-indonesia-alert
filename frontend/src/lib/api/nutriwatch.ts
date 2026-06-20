import { useQuery } from "@tanstack/react-query";
import { toast } from "sonner";

export const API_BASE =
  (typeof import.meta !== "undefined" && (import.meta as any).env?.VITE_API_BASE) ||
  "http://localhost:5000";

export type Stats = {
  region: string;
  total_texts_processed: number;
  total_signals_detected: number;
  total_incidents_recorded: number;
  match_rate_pct: number;
  avg_lag_days: number;
};

export type Aspect = {
  aspect: string;
  negative_pct: number;
  total_mentions: number;
};

export type Signal = {
  id: string;
  window_date: string;
  region: string;
  anomaly_score: number;
  is_signal: boolean;
  tweet_volume: number;
  negative_ratio: number;
  dominant_aspect: string;
};

export type Incident = {
  id: string;
  date: string;
  location: string;
  region: string;
  victim_count: number;
};

export type PipelineStatus = {
  stream_healthy: boolean;
  spark_throughput_rps: number;
  kafka_topics: Array<{ name: string; lag?: number; rps?: number } | string>;
};

let lastErrorToast = 0;
function notifyError(label: string, err: unknown) {
  const now = Date.now();
  if (now - lastErrorToast < 4000) return;
  lastErrorToast = now;
  toast.error(`Backend tidak terjangkau`, {
    description: `Gagal memuat ${label}. Pastikan API berjalan di ${API_BASE}.`,
  });
  console.error(`[NutriWatch API] ${label}`, err);
}

async function fetchJson<T>(path: string, label: string): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      headers: { Accept: "application/json" },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return (await res.json()) as T;
  } catch (err) {
    notifyError(label, err);
    throw err;
  }
}

export function useStats() {
  return useQuery({
    queryKey: ["nw", "stats"],
    queryFn: () => fetchJson<Stats>("/api/stats", "statistik"),
    staleTime: 30_000,
    retry: 1,
  });
}

export function useAspects(days = 30) {
  return useQuery({
    queryKey: ["nw", "aspects", days],
    queryFn: () => fetchJson<Aspect[]>(`/api/aspects?days=${days}`, "aspek sentimen"),
    staleTime: 30_000,
    retry: 1,
  });
}

export function useSignals(days = 30) {
  return useQuery({
    queryKey: ["nw", "signals", days],
    queryFn: () => fetchJson<Signal[]>(`/api/signals?days=${days}`, "sinyal anomali"),
    staleTime: 15_000,
    refetchInterval: 30_000,
    retry: 1,
  });
}

export function useIncidents(days = 30) {
  return useQuery({
    queryKey: ["nw", "incidents", days],
    queryFn: () => fetchJson<Incident[]>(`/api/incidents?days=${days}`, "insiden historis"),
    staleTime: 60_000,
    retry: 1,
  });
}

export function usePipelineStatus() {
  return useQuery({
    queryKey: ["nw", "pipeline-status"],
    queryFn: () => fetchJson<PipelineStatus>("/api/pipeline-status", "status pipeline"),
    refetchInterval: 20_000,
    retry: 1,
  });
}

// --- helpers ---
export const ASPECT_LABELS: Record<string, string> = {
  rasa_menu: "Rasa & Menu",
  porsi_kecukupan: "Porsi & Kecukupan",
  distribusi_ketepatan: "Distribusi & Ketepatan",
  higienitas_keamanan: "Higienitas & Keamanan",
};

// Rough centroid coordinates for known Indonesian regions to plot incidents.
const REGION_COORDS: Record<string, [number, number]> = {
  jawa: [-7.5, 110.5],
  "jawa barat": [-6.914, 107.61],
  "jawa tengah": [-7.15, 110.14],
  "jawa timur": [-7.536, 112.238],
  "dki jakarta": [-6.2, 106.816],
  jakarta: [-6.2, 106.816],
  banten: [-6.4, 106.064],
  yogyakarta: [-7.797, 110.37],
  "di yogyakarta": [-7.797, 110.37],
  bali: [-8.34, 115.092],
  "sumatera utara": [3.595, 98.672],
  "sumatera barat": [-0.95, 100.35],
  "sumatera selatan": [-3.32, 104.76],
  aceh: [4.695, 96.749],
  riau: [0.293, 101.706],
  lampung: [-5.45, 105.27],
  "kalimantan barat": [-0.026, 109.342],
  "kalimantan timur": [-0.5, 117.15],
  "kalimantan selatan": [-3.092, 115.283],
  "sulawesi selatan": [-5.147, 119.432],
  "sulawesi utara": [1.474, 124.842],
  papua: [-4.27, 138.08],
  "papua barat": [-1.336, 133.174],
  ntt: [-8.658, 121.079],
  ntb: [-8.652, 117.361],
  maluku: [-3.238, 130.145],
};

export function coordsForRegion(region: string): [number, number] {
  const key = region.trim().toLowerCase();
  if (REGION_COORDS[key]) return REGION_COORDS[key];
  // partial match
  for (const k of Object.keys(REGION_COORDS)) {
    if (key.includes(k) || k.includes(key)) return REGION_COORDS[k];
  }
  return [-2.5, 117]; // Indonesia center fallback
}
