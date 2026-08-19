"use client";

import React, { useState } from "react";
import { MessageSquare, Sparkles, BookOpen, ChevronDown, ChevronUp, CheckCircle } from "lucide-react";

export interface CitedChunkProps {
  id: string;
  text: string;
  score: number;
  doc_id: string;
  lang: string;
  strategy: string;
}

interface ResponseCardProps {
  query: string;
  answer: string;
  language: string;
  citedChunks: CitedChunkProps[];
}

export const ResponseCard: React.FC<ResponseCardProps> = ({ query, answer, language, citedChunks }) => {
  const [showSources, setShowSources] = useState(false);

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 backdrop-blur-xl shadow-xl space-y-4">
      <div className="flex items-start gap-3 pb-3 border-b border-slate-800/80">
        <div className="h-8 w-8 rounded-lg bg-indigo-950 border border-indigo-800 flex items-center justify-center flex-shrink-0 mt-0.5">
          <MessageSquare className="h-4 w-4 text-indigo-400" />
        </div>
        <div className="flex-1">
          <span className="text-[11px] font-semibold text-indigo-400 uppercase tracking-wider">
            Recognized Query ({language})
          </span>
          <p className="text-sm font-medium text-slate-200 mt-0.5">{query}</p>
        </div>
      </div>

      <div className="flex items-start gap-3">
        <div className="h-8 w-8 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center flex-shrink-0 mt-0.5">
          <Sparkles className="h-4 w-4 text-emerald-400" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">
              Grounded RAG Answer
            </span>
            <span className="inline-flex items-center gap-1 text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-800 px-1.5 py-0.2 rounded">
              <CheckCircle className="h-2.5 w-2.5" /> Grounded
            </span>
          </div>
          <p className="text-base text-slate-100 mt-1 leading-relaxed">{answer}</p>
        </div>
      </div>

      {citedChunks && citedChunks.length > 0 && (
        <div className="pt-2">
          <button
            onClick={() => setShowSources(!showSources)}
            className="flex items-center justify-between w-full px-3 py-2 bg-slate-950/70 border border-slate-800/80 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition-colors"
          >
            <div className="flex items-center gap-2">
              <BookOpen className="h-3.5 w-3.5 text-indigo-400" />
              <span>Cited MSMARCO-XI Knowledge Chunks ({citedChunks.length})</span>
            </div>
            {showSources ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </button>

          {showSources && (
            <div className="mt-2 space-y-2">
              {citedChunks.map((chunk, idx) => (
                <div
                  key={chunk.id || idx}
                  className="bg-slate-950/90 border border-slate-800/90 rounded-lg p-3 text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] text-indigo-400 font-semibold">
                      [{chunk.id}]
                    </span>
                    <span className="text-[10px] bg-indigo-950 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-800">
                      Similarity: {(chunk.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-slate-300 leading-relaxed font-sans">{chunk.text}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
