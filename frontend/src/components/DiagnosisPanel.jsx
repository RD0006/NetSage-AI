import { useEffect, useState } from "react";

function DiagnosisPanel({ diagnosis }) {
  const [currentDiagnosis, setCurrentDiagnosis] = useState(null);
  const [editing, setEditing] = useState(false);
  const [reviewStatus, setReviewStatus] = useState(null);

  useEffect(() => {
    if (!diagnosis) {
      setCurrentDiagnosis(null);
      setReviewStatus(null);
      setEditing(false);
      return;
    }

    setCurrentDiagnosis({
      ...diagnosis,
      evidence: [...(diagnosis.evidence || [])],
      next_command: [...(diagnosis.next_command || [])],
      fix_steps: [...(diagnosis.fix_steps || [])],
    });

    setReviewStatus(null);
    setEditing(false);
  }, [diagnosis]);

  if (!currentDiagnosis) {
    return (
      <div className="rounded-2xl border border-white/10 bg-[#0d1117] p-6">
        <h2 className="text-lg font-semibold">Diagnosis</h2>
        <p className="mt-3 text-sm text-gray-500">
          Run an analysis to see the network diagnosis.
        </p>
      </div>
    );
  }

  const handleAccept = () => {
    setReviewStatus("Accepted");
    setEditing(false);
  };

  const handleReject = () => {
    setReviewStatus("Rejected");
    setEditing(false);
  };

  const handleEdit = () => {
    setEditing(true);
    setReviewStatus(null);
  };

  const handleSaveEdit = () => {
    setEditing(false);
    setReviewStatus("Edited");
  };

  const updateField = (field, value) => {
    setCurrentDiagnosis((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const statusClass =
    reviewStatus === "Accepted"
      ? "border-green-500/30 bg-green-500/10 text-green-400"
      : reviewStatus === "Rejected"
      ? "border-red-500/30 bg-red-500/10 text-red-400"
      : reviewStatus === "Edited"
      ? "border-sky-500/30 bg-sky-500/10 text-sky-400"
      : "border-yellow-500/30 bg-yellow-500/10 text-yellow-400";

  return (
    <div className="rounded-2xl border border-white/10 bg-[#0d1117] p-6 shadow-xl">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-sky-400">
            AI Analysis
          </p>
          <h2 className="mt-1 text-xl font-bold">Diagnosis</h2>
        </div>

        <div
          className={`rounded-full border px-3 py-1 text-xs font-semibold ${statusClass}`}
        >
          {reviewStatus || "Review Required"}
        </div>
      </div>

      <div className="mt-5 rounded-xl border border-white/10 bg-black/20 p-4">
        {!reviewStatus && (
          <p className="text-sm text-yellow-400">
            Human review is required before this diagnosis is accepted.
          </p>
        )}

        {reviewStatus === "Accepted" && (
          <p className="text-sm text-green-400">
            Diagnosis accepted by human reviewer.
          </p>
        )}

        {reviewStatus === "Rejected" && (
          <p className="text-sm text-red-400">
            Diagnosis rejected by human reviewer.
          </p>
        )}

        {reviewStatus === "Edited" && (
          <p className="text-sm text-sky-400">
            Diagnosis edited. Please accept or reject the revised diagnosis.
          </p>
        )}
      </div>

      <div className="mt-6">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Likely Fault
        </p>

        {editing ? (
          <textarea
            value={currentDiagnosis.root_cause}
            onChange={(e) =>
              updateField("root_cause", e.target.value)
            }
            className="mt-2 w-full rounded-lg border border-white/10 bg-black/30 p-3 text-sm text-white outline-none focus:border-sky-500"
            rows={3}
          />
        ) : (
          <p className="mt-2 text-sm leading-6 text-gray-200">
            {currentDiagnosis.root_cause}
          </p>
        )}
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Confidence Level
        </p>
        <p className="mt-2 text-sm font-medium text-gray-200">
          {currentDiagnosis.confidence}
        </p>
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          OSI Layer
        </p>
        <p className="mt-2 text-sm text-gray-200">
          {currentDiagnosis.osi_layer}
        </p>
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Fault Domain
        </p>
        <p className="mt-2 text-sm text-gray-200">
          {currentDiagnosis.fault_domain}
        </p>
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Suggested Next Command
        </p>

        {currentDiagnosis.next_command?.length > 0 ? (
          <div className="mt-2 space-y-2">
            {currentDiagnosis.next_command.map((command, index) => (
              <code
                key={index}
                className="block rounded-lg bg-black/40 p-3 text-sm text-sky-300"
              >
                {command}
              </code>
            ))}
          </div>
        ) : (
          <p className="mt-2 text-sm text-gray-500">
            No additional command required.
          </p>
        )}
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Evidence
        </p>

        <ul className="mt-2 space-y-2">
          {currentDiagnosis.evidence?.map((item, index) => (
            <li
              key={index}
              className="text-sm leading-5 text-gray-300"
            >
              • {item}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-gray-500">
          Recommended Fix
        </p>

        {editing ? (
          <textarea
            value={currentDiagnosis.fix_steps.join("\n")}
            onChange={(e) =>
              updateField(
                "fix_steps",
                e.target.value
                  .split("\n")
                  .filter((step) => step.trim())
              )
            }
            className="mt-2 w-full rounded-lg border border-white/10 bg-black/30 p-3 text-sm text-white outline-none focus:border-sky-500"
            rows={5}
          />
        ) : (
          <ol className="mt-2 space-y-2">
            {currentDiagnosis.fix_steps?.map((step, index) => (
              <li
                key={index}
                className="text-sm leading-5 text-gray-300"
              >
                {index + 1}. {step}
              </li>
            ))}
          </ol>
        )}
      </div>

      <div className="mt-7 flex gap-3 border-t border-white/10 pt-5">
        {editing ? (
          <button
            type="button"
            onClick={handleSaveEdit}
            className="flex-1 cursor-pointer rounded-lg bg-sky-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-sky-400"
          >
            Save Edit
          </button>
        ) : (
          <>
            <button
              type="button"
              onClick={handleEdit}
              className="flex-1 cursor-pointer rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm font-semibold text-gray-200 transition hover:bg-white/10"
            >
              Edit
            </button>

            <button
              type="button"
              onClick={handleReject}
              className="flex-1 rounded-lg cursor-pointer border border-red-500/30 bg-red-500/10 px-4 py-2.5 text-sm font-semibold text-red-400 transition hover:bg-red-500/20"
            >
              Reject
            </button>

            <button
              type="button"
              onClick={handleAccept}
              className="flex-1 cursor-pointer rounded-lg bg-green-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-green-400"
            >
              Accept
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default DiagnosisPanel;