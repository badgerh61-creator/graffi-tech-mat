// src/pages/Home.jsx
import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <div className="min-h-screen bg-app text-ui-text overflow-hidden">

      {/* --- Floating Gradient Background Lights --- */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute -top-20 -left-24 w-96 h-96 bg-indigo-400/20 blur-3xl rounded-full" />
        <div className="absolute top-40 right-0 w-80 h-80 bg-fuchsia-400/20 blur-3xl rounded-full" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-10">

        {/* HEADER */}
        <header className="flex items-center justify-between mb-20">
          <motion.h1
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-3xl font-bold tracking-tight"
          >
            Graffi-Tech-Mat
          </motion.h1>

          <nav className="flex items-center gap-5 text-sm">
            <Link
              to="/"
              className="opacity-70 hover:opacity-100 transition"
            >
              Home
            </Link>

            <Link
              to="/studio"
              className="btn-primary px-5 py-2"
            >
              Open Studio
            </Link>
          </nav>
        </header>

        {/* MAIN HERO SECTION */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">

          {/* LEFT CONTENT */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-5xl font-black leading-[1.15] mb-6">
              Professional <span className="text-ui-accent">Material Studio</span>
            </h2>

            <p className="opacity-80 text-lg leading-relaxed mb-8 max-w-md">
              Import 3D models, edit physically-based materials with real-time
              lighting, manage HDRIs, save presets and export production packs.
              Designed for artists, developers, and creators.
            </p>

            <div className="flex items-center gap-4">
              <Link to="/studio" className="btn-primary text-base px-6 py-3">
                Enter Studio
              </Link>
              <a
                href="#"
                className="text-sm opacity-60 hover:opacity-100 transition"
              >
                Documentation
              </a>
            </div>
          </motion.div>

          {/* RIGHT VISUAL PREVIEW CARD */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7 }}
            className="relative"
          >
            {/* Card Container */}
            <div className="p-6 rounded-3xl bg-ui-surface border border-ui-border card-shadow relative overflow-hidden">

              {/* animated light sweep */}
              <motion.div
                initial={{ x: "-100%" }}
                animate={{ x: "150%" }}
                transition={{
                  repeat: Infinity,
                  duration: 4,
                  ease: "linear",
                }}
                className="absolute top-0 left-0 w-1/3 h-full bg-white/5 backdrop-blur-sm rotate-12"
              />

              <div className="w-full h-56 rounded-2xl bg-gradient-to-br from-slate-300/40 to-slate-500/40 flex items-center justify-center">
                <div className="text-lg opacity-50">Studio Preview</div>
              </div>

              <p className="text-sm opacity-60 mt-4">
                Ultra-clean UI for professional workflow.
              </p>
            </div>
          </motion.div>

        </section>

        {/* FEATURES GRID */}
        <motion.section
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <FeatureCard title="Real-Time Rendering" desc="Physically accurate PBR workflow with HDRI lighting." />
          <FeatureCard title="Universal Upload" desc="Import GLB, OBJ, FBX, PNG, HDR, textures & more." />
          <FeatureCard title="Preset System" desc="Save, load, edit and share material libraries." />
        </motion.section>

        {/* FOOTER */}
        <footer className="mt-24 text-xs opacity-60 text-center">
          © {new Date().getFullYear()} Graffi-Tech-Mat — All Rights Reserved.
        </footer>
      </div>
    </div>
  );
}

/* --- Small Reusable FeatureCard Component --- */
function FeatureCard({ title, desc }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="rounded-2xl bg-ui-surface border border-ui-border card-shadow p-6"
    >
      <div className="text-lg font-semibold mb-2">{title}</div>
      <p className="text-sm opacity-70 leading-relaxed">{desc}</p>
    </motion.div>
  );
}
