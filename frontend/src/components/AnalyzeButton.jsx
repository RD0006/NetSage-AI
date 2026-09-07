function AnalyzeButton({ loading, onClick }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="w-full cursor-pointer rounded-xl bg-sky-400 px-6 py-4 font-semibold text-slate-950 transition hover:bg-sky-300 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {loading
        ? "Analyzing Network..."
        : "Analyze Network →"}
    </button>
  );
}

export default AnalyzeButton;