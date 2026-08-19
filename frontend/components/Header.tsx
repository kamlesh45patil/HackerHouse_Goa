"use client";

import React from "react";
import { Mic, Zap } from "lucide-react";

export const Header: React.FC = () => {
  return (
    <header className="border-b border-slate-800 bg-slate-950/70 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Mic className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-bold text-lg text-white tracking-tight">Voice RAG System</h1>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-900/60 text-indigo-300 border border-indigo-700/50">
                Hacker House Goa 2026
              </span>
            </div>
            <p className="text-xs text-slate-400">Multilingual Indic Passage QA • FAISS + Sarvam + Gemini Flash</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-800/50 text-emerald-400 text-xs font-medium">
            <Zap className="h-3.5 w-3.5 text-emerald-400 animate-pulse" />
            <span>Target: &lt;200ms Core Pipeline</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping" />
            <span>System Live</span>
          </div>
        </div>
      </div>
    </header>
  );
};
