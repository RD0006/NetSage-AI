function ConnectionRow({
  connection,
  devices,
  onUpdate,
  onRemove,
}) {
  return (
    <div className="flex flex-col gap-3 rounded-xl border border-white/10 bg-[#0b1017] p-4 sm:flex-row sm:items-center">
      <select
        value={connection.from}
        onChange={(e) =>
          onUpdate(
            connection.id,
            "from",
            e.target.value
          )
        }
        className="input"
      >
        {devices.map((device) => (
          <option
            key={device.id}
            value={device.id}
          >
            {device.name}
          </option>
        ))}
      </select>

      <div className="text-center text-sky-400">
        →
      </div>

      <select
        value={connection.to}
        onChange={(e) =>
          onUpdate(
            connection.id,
            "to",
            e.target.value
          )
        }
        className="input"
      >
        {devices.map((device) => (
          <option
            key={device.id}
            value={device.id}
          >
            {device.name}
          </option>
        ))}
      </select>

      <button
        onClick={() => onRemove(connection.id)}
        className="text-xs cursor-pointer text-red-400 hover:text-red-300"
      >
        Remove
      </button>
    </div>
  );
}

export default ConnectionRow;