import { useEffect, useState } from "react";

function HistoryPanel({ onSelect }) {
  const [history, setHistory] = useState([]);

  const loadHistory = () => {
    const savedHistory = JSON.parse(
      localStorage.getItem("netsage_history") || "[]"
    );

    setHistory(savedHistory);
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const deleteEntry = (id) => {
    const updatedHistory = history.filter(
      (item) => item.id !== id
    );

    localStorage.setItem(
      "netsage_history",
      JSON.stringify(updatedHistory)
    );

    setHistory(updatedHistory);
  };

  const clearHistory = () => {
    localStorage.removeItem("netsage_history");
    setHistory([]);
  };

  return (
    <div className="rounded-2xl border border-white/10 bg-[#0d1117] p-6 shadow-xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-sky-400">
            Previous Analyses
          </p>

          <h2 className="mt-1 text-xl font-bold">
            History
          </h2>
        </div>

        {history.length > 0 && (
          <button
            type="button"
            onClick={clearHistory}
            className="text-xs font-semibold text-red-400 hover:text-red-300"
          >
            Clear All
          </button>
        )}
      </div>

      {history.length === 0 ? (
        <p className="mt-5 text-sm text-gray-500">
          No previous analyses found.
        </p>
      ) : (
        <div className="mt-5 space-y-3">
          {history.map((item) => (
            <div
              key={item.id}
              className="rounded-xl border border-white/10 bg-black/20 p-4"
            >
              <button
                type="button"
                onClick={() => onSelect(item)}
                className="w-full text-left"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-gray-200">
                      {item.symptom}
                    </p>

                    <p className="mt-1 text-xs text-gray-500">
                      {new Date(
                        item.timestamp
                      ).toLocaleString()}
                    </p>

                    <p className="mt-2 text-xs text-sky-400">
                      {item.diagnosis?.root_cause}
                    </p>
                  </div>

                  <span
                    className={`shrink-0 rounded-full border px-2 py-1 text-[10px] font-semibold ${
                      item.reviewStatus === "Accepted"
                        ? "border-green-500/30 bg-green-500/10 text-green-400"
                        : item.reviewStatus === "Rejected"
                        ? "border-red-500/30 bg-red-500/10 text-red-400"
                        : item.reviewStatus === "Edited"
                        ? "border-sky-500/30 bg-sky-500/10 text-sky-400"
                        : "border-yellow-500/30 bg-yellow-500/10 text-yellow-400"
                    }`}
                  >
                    {item.reviewStatus || "Review Required"}
                  </span>
                </div>
              </button>

              <div className="mt-3 border-t border-white/10 pt-3">
                <button
                  type="button"
                  onClick={() => deleteEntry(item.id)}
                  className="text-xs font-semibold text-red-400 hover:text-red-300"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default HistoryPanel;