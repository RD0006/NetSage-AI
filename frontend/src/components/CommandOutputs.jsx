import SectionHeader from "./SectionHeader";
import CommandOutputRow from "./CommandOutputRow";

function CommandOutputs({
  commands,
  onAdd,
  onUpdate,
  onRemove,
}) {
  return (
    <section className="card">
      <SectionHeader
        title="Show Command Outputs"
        description="Add Cisco commands and their corresponding outputs."
      />

      <div className="space-y-5">
        {commands.map((item, index) => (
          <CommandOutputRow
            key={item.id}
            item={item}
            index={index}
            canRemove={commands.length > 1}
            onUpdate={onUpdate}
            onRemove={onRemove}
          />
        ))}
      </div>

      <button
        onClick={onAdd}
        className="mt-5 cursor-pointer w-full rounded-xl border border-dashed border-white/20 py-3 text-sm text-gray-300 transition hover:border-sky-400/40 hover:text-sky-300"
      >
        + Add Another Command
      </button>
    </section>
  );
}

export default CommandOutputs;