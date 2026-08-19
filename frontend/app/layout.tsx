import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Voice-Enabled RAG System | Hacker House Goa 2026",
  description: "End-to-end multilingual voice RAG with FAISS, Sarvam STT, and Gemini Flash (<200ms target)",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
