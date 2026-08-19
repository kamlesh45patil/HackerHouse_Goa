"use client";

import React, { useState } from "react";
import { Mic, Square, Volume2, Globe, Radio } from "lucide-react";
import { useAudioRecorder } from "../hooks/useAudioRecorder";

interface VoiceRecorderProps {
  onAudioReady: (blob: Blob, language: string) => void;
  isLoading: boolean;
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({ onAudioReady, isLoading }) => {
  const { isRecording, duration, volumeLevel, startRecording, stopRecording } = useAudioRecorder();
  const [selectedLang, setSelectedLang] = useState("auto");

  const handleToggleRecord = async () => {
    if (isRecording) {
      const blob = await stopRecording();
      if (blob) {
        onAudioReady(blob, selectedLang);
      }
    } else {
      await startRecording();
    }
  };

  const formatTime = (secs: number) => {
    const mins = Math.floor(secs / 60);
    const remSecs = secs % 60;
    return `${mins}:${remSecs < 10 ? "0" : ""}${remSecs}`;
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-slate-900/60 border border-slate-800/80 rounded-2xl backdrop-blur-xl shadow-2xl relative overflow-hidden">
      <div className={`absolute -inset-1 rounded-2xl opacity-30 blur-2xl transition-all duration-700 pointer-events-none ${
        isRecording ? "bg-red-500/50" : isLoading ? "bg-indigo-500/40" : "bg-purple-600/20"
      }`} />

      <div className="flex items-center gap-2 mb-6 z-10">
        <Globe className="h-4 w-4 text-indigo-400" />
        <span className="text-xs text-slate-400 font-medium">Spoken Language:</span>
        <div className="flex bg-slate-950/80 border border-slate-800 rounded-lg p-0.5">
          {[
            { id: "auto", label: "Auto Detect" },
            { id: "hi-IN", label: "हिंदी (Hindi)" },
            { id: "en-IN", label: "English (IN)" }
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setSelectedLang(item.id)}
              className={`px-2.5 py-1 text-xs rounded-md transition-all ${
                selectedLang === item.id
                  ? "bg-indigo-600 text-white font-medium shadow"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      <div className="relative my-4 z-10 flex items-center justify-center">
        {isRecording && (
          <>
            <div
              className="absolute h-36 w-36 rounded-full bg-red-500/20 animate-ping pointer-events-none"
              style={{ transform: `scale(${1 + volumeLevel / 100})` }}
            />
            <div
              className="absolute h-48 w-48 rounded-full border border-red-500/30 animate-pulse pointer-events-none"
            />
          </>
        )}

        <button
          onClick={handleToggleRecord}
          disabled={isLoading}
          className={`h-28 w-28 rounded-full flex flex-col items-center justify-center transition-all duration-300 shadow-2xl relative z-10 ${
            isRecording
              ? "bg-gradient-to-tr from-red-600 to-rose-500 scale-105 shadow-red-600/40 animate-pulse"
              : isLoading
              ? "bg-slate-800 border-2 border-indigo-500/50 cursor-not-allowed opacity-75"
              : "bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-600 hover:scale-105 shadow-indigo-500/30 hover:shadow-indigo-500/50 cursor-pointer"
          }`}
        >
          {isRecording ? (
            <Square className="h-9 w-9 text-white fill-white" />
          ) : isLoading ? (
            <div className="h-8 w-8 border-3 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Mic className="h-10 w-10 text-white drop-shadow" />
          )}
        </button>
      </div>

      <div className="mt-4 flex flex-col items-center z-10">
        {isRecording ? (
          <div className="flex items-center gap-3 text-red-400 font-medium">
            <Radio className="h-4 w-4 animate-pulse" />
            <span className="text-sm tracking-wider font-mono font-bold">{formatTime(duration)}</span>
            <div className="flex items-center gap-1 h-3 bg-slate-950 px-2 py-0.5 rounded-full border border-red-900/50">
              <Volume2 className="h-3 w-3 text-red-400" />
              <div className="w-12 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-emerald-400 via-yellow-400 to-red-500 transition-all duration-75"
                  style={{ width: `${volumeLevel}%` }}
                />
              </div>
            </div>
          </div>
        ) : isLoading ? (
          <div className="flex items-center gap-2 text-indigo-400 text-sm animate-pulse">
            <span className="h-2 w-2 rounded-full bg-indigo-400" />
            <span>Processing Pipeline (STT → FAISS → Gemini → Guardrail)...</span>
          </div>
        ) : (
          <p className="text-xs text-slate-400">Click microphone to speak your question in Hindi or English</p>
        )}
      </div>
    </div>
  );
};
