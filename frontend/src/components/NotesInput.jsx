import SectionHeader from "./SectionHeader";

function NotesInput({ value, onChange }) {
  return (
    <section className="card">
      <SectionHeader
        title="Packet Tracer Notes / Context"
        description="Optional additional information about the lab."
      />

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Example: VLAN 10 should communicate with VLAN 20 through R1..."
        className="input min-h-[130px] resize-y"
      />
    </section>
  );
}

export default NotesInput;