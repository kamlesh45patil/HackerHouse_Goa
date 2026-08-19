"use client";

import React from "react";
import { ShieldX } from "lucide-react";

interface GuardrailAlertProps {
  reason: string;
  groundingScore?: number;
}

export const GuardrailAlert: React.FC<GuardrailAlertProps> = ({ reason, groundingScore }) => {
  return (
    <div className="bg-red-950/40 border border-red-800/80 rounded-2xl p-5 backdrop-blur-xl shadow-xl flex items-start gap-3.5">
      <div className="h-9 w-9 rounded-xl bg-red-900/60 border border-red-700 flex items-center justify-center flex-shrink-0 text-red-400">
        <ShieldX className="h-5 w-5" />
      </div>
      <div className="flex-1 space-y-1">
        <div className="flex items-center gap-2">
          <h4 className="text-xs font-bold text-red-400 uppercase tracking-wider">
            Safety / Grounding Guardrail Triggered
          </h4>
          {groundingScore !== undefined && groundingScore > 0 && (
            <span className="text-[10px] bg-red-900/60 text-red-300 px-1.5 py-0.5 rounded border border-red-700">
              Grounding: {(groundingScore * 100).toFixed(1)}%
            </span>
          )}
        </div>
        <p className="text-sm text-red-200">
          I do not have sufficient verified information in the retrieved knowledge base to answer this query accurately, or it was flagged by safety policies.
        </p>
        <p className="text-xs text-red-400/90 font-mono mt-1">Reason: {reason}</p>
      </div>
    </div>
  );
};
