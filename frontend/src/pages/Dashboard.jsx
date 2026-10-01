import React, { useState } from "react";
import { runResearch } from "../services/api";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [activeTab, setActiveTab] = useState("report");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setData(null);

    try {
      const result = await runResearch(query);
      setData(result);
      setActiveTab("report");
    } catch (err) {
      setError(err.message || "Failed to conduct research.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-6 flex flex-col items-center">
      <div className="w-full max-w-5xl">
        {/* Header */}
        <header className="text-center my-8">
          <h1 className="text-3xl font-bold tracking-tight text-slate-800">
            Autonomous AI Research Assistant
          </h1>
          <p className="text-slate-600 mt-2 text-sm">
            Live Web Search • Llama 3.2 Analysis • Fact Critique • Synthesis Report
          </p>
        </header>

        {/* Query Input Box */}
        <form onSubmit={handleSubmit} className="flex gap-3 mb-8">
          <input
            type="text"
            className="flex-1 px-4 py-3 bg-white border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="e.g. Current breakthroughs in multi-agent reinforcement learning..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow disabled:opacity-50 transition"
          >
            {loading ? "Researching..." : "Start Research"}
          </button>
        </form>

        {/* Error Notification */}
        {error && (
          <div className="p-4 mb-6 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex flex-col items-center justify-center p-12 space-y-4">
            <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-slate-500 text-sm font-medium animate-pulse">
              Coordinating search, analysis, critic review, and report agents...
            </p>
          </div>
        )}

        {/* Multi-Agent Output Container */}
        {data && (
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            {/* Tabs Header */}
            <div className="flex border-b border-slate-200 bg-slate-100">
              <button
                onClick={() => setActiveTab("report")}
                className={`flex-1 py-3 px-4 font-semibold text-sm transition ${
                  activeTab === "report"
                    ? "bg-white text-indigo-600 border-b-2 border-indigo-600"
                    : "text-slate-600 hover:bg-slate-200"
                }`}
              >
                Final Report
              </button>
              <button
                onClick={() => setActiveTab("critique")}
                className={`flex-1 py-3 px-4 font-semibold text-sm transition ${
                  activeTab === "critique"
                    ? "bg-white text-indigo-600 border-b-2 border-indigo-600"
                    : "text-slate-600 hover:bg-slate-200"
                }`}
              >
                Critic Review
              </button>
              <button
                onClick={() => setActiveTab("analysis")}
                className={`flex-1 py-3 px-4 font-semibold text-sm transition ${
                  activeTab === "analysis"
                    ? "bg-white text-indigo-600 border-b-2 border-indigo-600"
                    : "text-slate-600 hover:bg-slate-200"
                }`}
              >
                Analysis Notes
              </button>
              <button
                onClick={() => setActiveTab("sources")}
                className={`flex-1 py-3 px-4 font-semibold text-sm transition ${
                  activeTab === "sources"
                    ? "bg-white text-indigo-600 border-b-2 border-indigo-600"
                    : "text-slate-600 hover:bg-slate-200"
                }`}
              >
                Sources ({data.source_count})
              </button>
            </div>

            {/* Tab Body View */}
            <div className="p-6">
              {activeTab === "report" && (
                <div className="prose max-w-none whitespace-pre-wrap leading-relaxed text-slate-800 text-sm">
                  {data.report}
                </div>
              )}

              {activeTab === "critique" && (
                <div className="prose max-w-none whitespace-pre-wrap leading-relaxed text-slate-800 text-sm">
                  {data.critique}
                </div>
              )}

              {activeTab === "analysis" && (
                <div className="prose max-w-none whitespace-pre-wrap leading-relaxed text-slate-800 text-sm">
                  {data.analysis}
                </div>
              )}

              {activeTab === "sources" && (
                <div className="space-y-4">
                  {data.sources.map((src, idx) => (
                    <div
                      key={idx}
                      className="p-4 border border-slate-200 rounded-lg hover:border-indigo-300 transition"
                    >
                      <div className="flex justify-between items-center mb-1">
                        <a
                          href={src.url}
                          target="_blank"
                          rel="noreferrer"
                          className="font-semibold text-indigo-600 hover:underline text-sm"
                        >
                          {src.title}
                        </a>
                        <span className="text-xs bg-slate-200 text-slate-700 px-2 py-0.5 rounded">
                          Score: {Number(src.score).toFixed(2)}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mb-2">{src.domain}</p>
                      <p className="text-xs text-slate-600 line-clamp-3">{src.content}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}