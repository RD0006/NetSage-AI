import SectionHeader from "./SectionHeader";

function SymptomInput({ value, onChange }) {
  return (
    <section className="card">
      <SectionHeader
        title="Problem / Symptom"
        description="Describe what is going wrong in the network."
      />

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Example: PC1 receives an IP address but cannot ping the server..."
        className="input min-h-[140px] resize-y"
      />
    </section>
  );
}

export default SymptomInput;