import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, ShieldAlert, Activity, Database, Brain, ExternalLink } from "lucide-react";
import heroImg from "@/assets/hero-landing.jpg";
import article1 from "@/assets/article-1.jpg";
import article2 from "@/assets/article-2.jpg";
import article3 from "@/assets/article-3.jpg";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "NutriWatch — Early Warning System untuk Program MBG" },
      {
        name: "description",
        content:
          "Platform Big Data untuk pemantauan dini risiko keracunan pada program Makan Bergizi Gratis (MBG) Badan Gizi Nasional.",
      },
      { property: "og:title", content: "NutriWatch — Early Warning System MBG" },
      {
        property: "og:description",
        content:
          "Memantau jutaan sinyal dari dapur umum se-Indonesia untuk mencegah insiden keracunan sebelum terjadi.",
      },
    ],
  }),
  component: Landing,
});

import { useNews } from "@/lib/api/nutriwatch";

function Landing() {
  const { data: newsItems, isLoading: newsLoading } = useNews();

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Top bar */}
      <header className="bg-navy text-navy-foreground border-b border-gold/30">
        <div className="mx-auto max-w-[1400px] px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-gold/15 ring-1 ring-gold/40">
              <ShieldAlert className="h-5 w-5 text-gold" />
            </div>
            <span className="text-lg font-bold tracking-tight">
              <span className="text-gold">NutriWatch</span>
            </span>
          </Link>
          <Link
            to="/overview"
            className="inline-flex items-center gap-2 rounded-full bg-gold px-4 py-2 text-sm font-semibold text-gold-foreground hover:brightness-105 transition"
          >
            Buka Dashboard <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-navy text-navy-foreground">
        <img
          src={heroImg}
          alt="Peta Indonesia dengan visualisasi data"
          className="absolute inset-0 h-full w-full object-cover opacity-30"
          width={1920}
          height={1080}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-navy/80 via-navy/70 to-navy" />
        <div className="relative mx-auto max-w-[1400px] px-6 py-20 sm:py-28 grid lg:grid-cols-[1.2fr_1fr] gap-10 items-center">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-gold/15 text-gold ring-1 ring-gold/40 px-3 py-1 text-xs font-medium">
              <span className="h-1.5 w-1.5 rounded-full bg-gold animate-pulse" />
              Big Data · Early Warning · MBG
            </span>
            <h1 className="mt-5 text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-[1.05]">
              Mencegah Krisis Sebelum
              <br />
              <span className="text-gold">Piring Sampai ke Tangan Anak.</span>
            </h1>
            <p className="mt-6 max-w-2xl text-base sm:text-lg text-navy-foreground/75 leading-relaxed">
              NutriWatch memadukan streaming data, NLP berbahasa Indonesia, dan deteksi
              anomali untuk memberi peringatan dini risiko keracunan pada program
              Makan Bergizi Gratis di seluruh Indonesia.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/overview"
                className="inline-flex items-center gap-2 rounded-full bg-gold px-5 py-2.5 text-sm font-semibold text-gold-foreground hover:brightness-105 transition"
              >
                Lihat Dashboard Real-time <ArrowRight className="h-4 w-4" />
              </Link>
              <a
                href="#tentang"
                className="inline-flex items-center gap-2 rounded-full border border-navy-foreground/25 px-5 py-2.5 text-sm font-semibold text-navy-foreground hover:bg-navy-foreground/5 transition"
              >
                Tentang Proyek
              </a>
            </div>
          </div>
          <div className="hidden lg:grid grid-cols-2 gap-4">
            {[
              { icon: Activity, k: "12,480", v: "Dapur Umum Terpantau" },
              { icon: Database, k: "8.3 Jt", v: "Penerima Manfaat" },
              { icon: Brain, k: "17", v: "Red Flag Aktif" },
              { icon: ShieldAlert, k: "94.2%", v: "Zona Aman" },
            ].map(({ icon: Icon, k, v }) => (
              <div
                key={v}
                className="rounded-2xl border border-gold/20 bg-navy-foreground/[0.04] backdrop-blur p-4"
              >
                <Icon className="h-5 w-5 text-gold" />
                <div className="mt-3 text-2xl font-bold">{k}</div>
                <div className="text-xs text-navy-foreground/70">{v}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About */}
      <section id="tentang" className="mx-auto max-w-[1100px] px-6 py-20">
        <div className="max-w-2xl">
          <span className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">
            Tentang Proyek
          </span>
          <h2 className="mt-3 text-3xl sm:text-4xl font-bold tracking-tight">
            Mengapa NutriWatch Dibuat?
          </h2>
        </div>
        <div className="mt-8 grid md:grid-cols-2 gap-8 text-[15px] leading-relaxed text-muted-foreground">
          <p>
            NutriWatch lahir dari kebutuhan mendesak untuk melindungi jutaan anak-anak Indonesia yang menerima manfaat Program Makan Bergizi Gratis (MBG). Dengan skala nasional dan ribuan dapur umum yang terlibat, potensi risiko seperti higienitas makanan dan kecukupan gizi menjadi tantangan besar. Kami percaya pencegahan adalah kunci keselamatan mereka.
          </p>
          <p>
            Oleh karena itu, kami membangun infrastruktur Big Data real-time menggunakan Spark Streaming dan Elasticsearch. Sistem ini membaca jutaan suara publik secara langsung, menggunakan teknologi AI *Natural Language Processing* (IndoBERT) untuk memfilter sinyal bahaya keracunan atau keluhan porsi, lalu menampilkannya sebagai *Early Warning System* sebelum krisis menyebar.
          </p>
        </div>
      </section>

      {/* Articles */}
      <section className="bg-secondary/40 border-y border-border">
        <div className="mx-auto max-w-[1400px] px-6 py-20">
          <div className="flex items-end justify-between gap-4 flex-wrap">
            <div>
              <span className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">
                Liputan Terkait
              </span>
              <h2 className="mt-3 text-3xl sm:text-4xl font-bold tracking-tight">
                Insiden Keracunan dalam Program MBG
              </h2>
              <p className="mt-3 max-w-2xl text-sm text-muted-foreground">
                Kumpulan berita dan laporan publik yang menjadi konteks pembangunan
                sistem peringatan dini ini.
              </p>
            </div>
          </div>

          <div className="mt-10 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {newsLoading ? (
              <div className="col-span-full py-10 text-center text-sm text-muted-foreground">
                Memuat berita terkini dari Google News...
              </div>
            ) : !newsItems || newsItems.length === 0 ? (
              <div className="col-span-full py-10 text-center text-sm text-muted-foreground">
                Tidak ada berita terkait saat ini.
              </div>
            ) : (
              newsItems.map((a, idx) => (
                <article
                  key={idx}
                  className="group rounded-2xl border bg-card overflow-hidden shadow-sm hover:shadow-md transition flex flex-col"
                >
                  <div className="aspect-[16/10] overflow-hidden bg-muted relative">
                    <img
                      src={a.image || (idx === 0 ? article1 : idx === 1 ? article2 : article3)}
                      alt={a.title}
                      loading="lazy"
                      width={1024}
                      height={640}
                      className="h-full w-full object-cover group-hover:scale-[1.03] transition duration-500"
                    />
                  </div>
                  <div className="p-5 flex flex-col flex-1">
                    <span className="inline-flex w-fit items-center rounded-full bg-warn/10 text-warn ring-1 ring-warn/30 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider">
                      BERITA
                    </span>
                    <h3 className="mt-3 font-semibold text-base leading-snug line-clamp-2">
                      {a.title}
                    </h3>
                    <p className="mt-2 text-sm text-muted-foreground leading-relaxed flex-1 line-clamp-3">
                      {a.summary}
                    </p>
                    <a
                      href={a.link}
                      target="_blank"
                      rel="noreferrer"
                      className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-navy hover:text-gold transition"
                    >
                      Baca selengkapnya <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                    <div className="mt-2 text-[11px] text-muted-foreground flex justify-between">
                      <span>{a.source}</span>
                      <span>{new Date(a.published).toLocaleDateString("id-ID")}</span>
                    </div>
                  </div>
                </article>
              ))
            )}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-[1100px] px-6 py-20 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight">
          Pantau Risiko Secara Real-time.
        </h2>
        <p className="mt-4 text-muted-foreground max-w-xl mx-auto">
          Masuk ke dashboard NutriWatch untuk melihat zona risiko, red-flag alerts,
          dan analisis sentimen penerima manfaat.
        </p>
        <Link
          to="/overview"
          className="mt-8 inline-flex items-center gap-2 rounded-full bg-navy px-6 py-3 text-sm font-semibold text-navy-foreground hover:bg-navy/90 transition"
        >
          Buka Dashboard <ArrowRight className="h-4 w-4" />
        </Link>
      </section>

      <footer className="border-t border-border py-6 text-center text-[11px] text-muted-foreground">
        NutriWatch · Powered by Kafka · NiFi · Spark Streaming · IndoBERT · Elasticsearch
      </footer>
    </div>
  );
}
