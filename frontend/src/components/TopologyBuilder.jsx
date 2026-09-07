import SectionHeader from "./SectionHeader";
import DeviceCard from "./DeviceCard";
import ConnectionRow from "./ConnectionRow";

function TopologyBuilder({
  devices,
  connections,
  onAddDevice,
  onUpdateDevice,
  onRemoveDevice,
  onAddConnection,
  onUpdateConnection,
  onRemoveConnection,
}) {
  return (
    <section className="card">
      <SectionHeader
        title="Packet Tracer Topology"
        description="Add devices and define how they are connected."
      />

      {/* DEVICES */}

      <div className="grid gap-4 sm:grid-cols-2">
        {devices.map((device) => (
          <DeviceCard
            key={device.id}
            device={device}
            canRemove={devices.length > 2}
            onUpdate={onUpdateDevice}
            onRemove={onRemoveDevice}
          />
        ))}
      </div>

      <button
        onClick={onAddDevice}
        className="mt-5 w-full cursor-pointer rounded-xl border border-dashed border-sky-400/30 bg-sky-400/5 py-3 text-sm font-medium text-sky-300 transition hover:border-sky-400/60 hover:bg-sky-400/10"
      >
        + Add Device
      </button>

      {/* CONNECTIONS */}

      <div className="mt-8">
        <div className="mb-4 flex items-center justify-between">
          <h4 className="text-sm font-semibold">
            Connections
          </h4>

          <button
            onClick={onAddConnection}
            className="text-sm cursor-pointer text-sky-400 hover:text-sky-300"
          >
            + Add Connection
          </button>
        </div>

        <div className="space-y-3">
          {connections.map((connection) => (
            <ConnectionRow
              key={connection.id}
              connection={connection}
              devices={devices}
              onUpdate={onUpdateConnection}
              onRemove={onRemoveConnection}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default TopologyBuilder;