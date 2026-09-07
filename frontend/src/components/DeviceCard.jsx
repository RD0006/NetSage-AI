const deviceTypes = [
  "PC",
  "Router",
  "Switch",
  "Server",
  "Access Point",
  "Firewall",
];

function DeviceCard({
  device,
  canRemove,
  onUpdate,
  onRemove,
}) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#0b1017] p-4">
      <div className="mb-4 flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-gray-500">
          Device
        </span>

        {canRemove && (
          <button
            onClick={() => onRemove(device.id)}
            className="text-xs cursor-pointer text-red-400 hover:text-red-300"
          >
            Remove
          </button>
        )}
      </div>

      <input
        value={device.name}
        onChange={(e) =>
          onUpdate(
            device.id,
            "name",
            e.target.value
          )
        }
        className="input mb-3"
        placeholder="Device name"
      />

      <select
        value={device.type}
        onChange={(e) =>
          onUpdate(
            device.id,
            "type",
            e.target.value
          )
        }
        className="input"
      >
        {deviceTypes.map((type) => (
          <option key={type}>{type}</option>
        ))}
      </select>
    </div>
  );
}

export default DeviceCard;