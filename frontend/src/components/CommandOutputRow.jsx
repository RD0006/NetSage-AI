function CommandOutputRow({
  item,
  index,
  canRemove,
  onUpdate,
  onRemove,
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#0b1017] p-5">
      <div className="mb-4 flex items-center justify-between">
        <span className="text-xs font-medium text-gray-500">
          COMMAND {index + 1}
        </span>

        {canRemove && (
          <button
            onClick={() => onRemove(item.id)}
            className="text-xs cursor-pointer text-red-400 hover:text-red-300"
          >
            Remove
          </button>
        )}
      </div>

      <input
        value={item.command}
        onChange={(e) =>
          onUpdate(
            item.id,
            "command",
            e.target.value
          )
        }
        placeholder="e.g. show ip interface brief"
        className="input mb-3 font-mono"
      />

      <textarea
        value={item.output}
        onChange={(e) =>
          onUpdate(
            item.id,
            "output",
            e.target.value
          )
        }
        placeholder="Paste command output here..."
        className="input min-h-[160px] resize-y font-mono text-sm"
      />
    </div>
  );
}

export default CommandOutputRow;