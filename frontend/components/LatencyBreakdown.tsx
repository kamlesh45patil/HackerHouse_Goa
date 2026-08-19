"use client";

import React from "react";
import { Clock, Cpu, Database, ShieldCheck, Zap } from "lucide-react";

export interface LatenciesProps {
  stt_ms: number;
  retrieval_ms: number;
  generation_ms: number;
  guardrail_ms: number;
  core_pipeline_ms: number;
  total_ms: number;
}

export const LatencyBreakdown: React.FC<{ latencies: LatenciesProps }> = ({ latencies }) => {
  const isTargetMet = latencies.core_pipeline_ms <= 200;

  const getStatusBadge = (ms: number, budget: number) => {
    if (ms <= budget) {
      return "bg-emerald-950/70 border-emerald-700/50 text-emerald-400";
    } else if (ms <= budget * 1.3) {
      return "bg-yellow-950/70 border-yellow-700/50 text-yellow-400";
    } else {
      return "bg-red-950/70 border-red-700/50 text-red-400";
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 backdrop-blur-md">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-3">
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-indigo-400" />
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            Pipeline Latency Telemetry
          </h3>
        </div>
        <div
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-bold border ${
            isTargetMet
              ? "bg-emerald-950/80 border-emerald-600 text-emerald-300"
              : "bg-red-950/80 border-red-600 text-red-300"
          }`}
        >
          <Zap className="h-3 w-3" />
          <span>Core: {latencies.core_pipeline_ms.toFixed(1)} ms</span>
          <span className="text-[10px] font-normal opacity-80">
            ({isTargetMet ? "Target <200ms MET ✅" : "Over Budget ⚠️"})
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2.5 flex flex-col">
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <span className="h-1.5 w-1.5 rounded-full bg-sky-400" /> STT (Sarvam)
          </span>
          <span className="text-base font-mono font-bold text-slate-200 mt-1">
            {latencies.stt_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
          </span>
          <span className="text-[10px] text-slate-400 mt-0.5">Upstream Audio</span>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2.5 flex flex-col">
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <Database className="h-3 w-3 text-indigo-400" /> FAISS Lookup
          </span>
          <span className="text-base font-mono font-bold text-slate-200 mt-1">
            {latencies.retrieval_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
          </span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded mt-0.5 border w-fit ${getStatusBadge(latencies.retrieval_ms, 50)}`}>
            Budget: 50ms
          </span>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2.5 flex flex-col">
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <Cpu className="h-3 w-3 text-purple-400" /> Gemini Flash
          </span>
          <span className="text-base font-mono font-bold text-slate-200 mt-1">
            {latencies.generation_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
          </span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded mt-0.5 border w-fit ${getStatusBadge(latencies.generation_ms, 140)}`}>
            Budget: 140ms
          </span>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2.5 flex flex-col">
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <ShieldCheck className="h-3 w-3 text-emerald-400" /> Guardrails
          </span>
          <span className="text-base font-mono font-bold text-slate-200 mt-1">
            {latencies.guardrail_ms.toFixed(1)} <span className="text-xs font-normal text-slate-400">ms</span>
          </span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded mt-0.5 border w-fit ${getStatusBadge(latencies.guardrail_ms, 20)}`}>
            Budget: 20ms
          </span>
        </div>
      </div>
    </div>
  );
};
