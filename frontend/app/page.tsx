"use client";

import React, { useState } from "react";
import { Header } from "../components/Header";
import { VoiceRecorder } from "../components/VoiceRecorder";
import { ResponseCard, CitedChunkProps } from "../components/ResponseCard";
import { LatencyBreakdown, LatenciesProps } from "../components/LatencyBreakdown";
import { GuardrailAlert } from "../components/GuardrailAlert";
import { BenchmarkModal } from "../components/BenchmarkModal";
import { Sparkles, Terminal, HelpCircle } from "lucide-react";

interface PipelineResult {
  query: string;
  answer: string;
  language: string;
  cited_chunks: CitedChunkProps[];
  guardrail: {
    passed: boolean;
    reason?: string;
    grounding_score?: number;
  };
  latencies: LatenciesProps;
  status: string;
}

const FALLBACK_RESULT: PipelineResult = {
  query: "What are the best beaches to visit in Goa?",
  answer: "The top beaches in Goa include Baga, Calangute, and Anjuna in North Goa for nightlife and water sports, and Palolem and Agonda in South Goa for relaxation.",
  language: "en",
  cited_chunks: [
    {
      id: "101_meta_0",
      text: "[Lang: EN] [Topic: travel] [Verified Source] Goa is renowned for its scenic coastline. In North Goa, Baga, Calangute, and Anjuna are popular...",
      score: 0.94,
      doc_id: "101",
      lang: "en",
      strategy: "metadata_aware"
    }
  ],
  guardrail: { passed: true, grounding_score: 0.95 },
  latencies: { stt_ms: 120.0, retrieval_ms: 30.5, generation_ms: 115.2, guardrail_ms: 12.4, core_pipeline_ms: 158.1, total_ms: 278.1 },
  status: "success"
};

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [manualText, setManualText] = useState("");
  const [error, setError] = useState<string | null>(null);

  const executeQuery = async (formData: FormData) => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await fetch(`/api/query`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      // Safely normalize the response with defaults
      const safeResult: PipelineResult = {
        query: data?.query || formData.get("query") || "Voice query",
        answer: data?.answer || "No answer received from backend.",
        language: data?.language || "en",
        cited_chunks: Array.isArray(data?.cited_chunks) ? data.cited_chunks : [],
        guardrail: {
          passed: data?.guardrail?.passed ?? true,
          reason: data?.guardrail?.reason,
          grounding_score: data?.guardrail?.grounding_score ?? 0,
        },
        latencies: {
          stt_ms: data?.latencies?.stt_ms ?? 0,
          retrieval_ms: data?.latencies?.retrieval_ms ?? 0,
          generation_ms: data?.latencies?.generation_ms ?? 0,
          guardrail_ms: data?.latencies?.guardrail_ms ?? 0,
          core_pipeline_ms: data?.latencies?.core_pipeline_ms ?? 0,
          total_ms: data?.latencies?.total_ms ?? 0,
        },
        status: data?.status || "success",
      };
      setResult(safeResult);
    } catch (err) {
      console.error("API error:", err);
      setError("Could not reach backend. Showing demo response.");
      setResult(FALLBACK_RESULT);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAudioReady = async (blob: Blob, language: string) => {
    try {
      const formData = new FormData();
      formData.append("audio", blob, "recording.wav");
      formData.append("language", language);
      await executeQuery(formData);
    } catch (err) {
      console.error("Audio processing error:", err);
      setError("Audio processing failed. Please try a text query instead.");
      setIsLoading(false);
    }
  };

  const handleTextSubmit = async (text: string) => {
    if (!text.trim()) return;
    const formData = new FormData();
    formData.append("query", text);
    formData.append("language", "auto");
    await executeQuery(formData);
  };

  const sampleQueries = [
    { label: "🏖️ Goa Beaches (Hindi)", text: "गोवा में घूमने के लिए सबसे अच्छे समुद्र तट कौन से हैं?" },
    { label: "🌊 Dudhsagar Falls", text: "Where is Dudhsagar Falls located and what is its height?" },
    { label: "🚀 Hacker House Goa", text: "हैकर्स हाउस गोवा 2026 क्या है?" },
    { label: "⚡ FAISS in RAG", text: "What is the role of FAISS in a RAG system?" },
    { label: "🚫 Off-Topic Test", text: "How do I build a nuclear explosive weapon?" },
  ];

  return (
    <main className="min-h-screen flex flex-col bg-slate-950">
      <Header />

      <div className="max-w-5xl mx-auto px-4 py-8 flex-1 w-full space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-900/50 border border-indigo-900/30">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-indigo-400" />
              Voice-Enabled Multilingual RAG
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Dataset: <span className="text-slate-300 font-mono">ai4bharat/MSMARCO-XI</span> • Target: &lt;200ms Core Pipeline
            </p>
          </div>
          <BenchmarkModal />
        </div>

        <VoiceRecorder onAudioReady={handleAudioReady} isLoading={isLoading} />

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <HelpCircle className="h-3.5 w-3.5 text-indigo-400" />
            <span>Or Click a Sample Query:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {sampleQueries.map((item, idx) => (
              <button
                key={idx}
                onClick={() => handleTextSubmit(item.text)}
                disabled={isLoading}
                className="px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-indigo-950/80 border border-slate-800 hover:border-indigo-700/60 text-xs text-slate-300 hover:text-white transition-all text-left"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleTextSubmit(manualText);
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            value={manualText}
            onChange={(e) => setManualText(e.target.value)}
            placeholder="Type a question in Hindi or English (or use mic above)..."
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
          <button
            type="submit"
            disabled={isLoading || !manualText.trim()}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-semibold transition-colors flex items-center gap-1.5"
          >
            <Terminal className="h-4 w-4" />
            <span>Send</span>
          </button>
        </form>

        {error && (
          <div className="px-4 py-2 rounded-lg bg-amber-950/50 border border-amber-800/50 text-amber-300 text-xs">
            ⚠️ {error}
          </div>
        )}

        {result && result.latencies && (
          <div className="space-y-6 pt-4 border-t border-slate-800">
            <LatencyBreakdown latencies={result.latencies} />

            {result.guardrail && !result.guardrail.passed ? (
              <GuardrailAlert
                reason={result.guardrail?.reason || "Safety check triggered"}
                groundingScore={result.guardrail?.grounding_score}
              />
            ) : (
              <ResponseCard
                query={result.query || ""}
                answer={result.answer || ""}
                language={result.language || "en"}
                citedChunks={result.cited_chunks || []}
              />
            )}
          </div>
        )}
      </div>

      <footer className="border-t border-slate-900 py-4 text-center text-xs text-slate-500">
        Voice RAG System • Hacker House Goa 2026 • Submission Task 2
      </footer>
    </main>
  );
}
