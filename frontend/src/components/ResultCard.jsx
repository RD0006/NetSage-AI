function ResultCard({ title, value, mono = false }) {
  return (
    <div className="rounded-xl border border-white/5 bg-[#080b10] p-4">
      <p className="mb-2 text-xs font-medium uppercase tracking-wider text-gray-600">
        {title}
      </p>

      <p
        className={`text-sm leading-6 text-gray-300 ${
          mono
            ? "font-mono text-sky-300"
            : ""
        }`}
      >
        {value}
      </p>
    </div>
  );
}

export default ResultCard;