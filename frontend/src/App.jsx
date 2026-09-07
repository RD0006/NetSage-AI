// App.jsx

import { useState } from "react";

import Navbar from "./components/Navbar";
import SymptomInput from "./components/SymptomInput";
import TopologyBuilder from "./components/TopologyBuilder";
import CommandOutputs from "./components/CommandOutputs";
import NotesInput from "./components/NotesInput";
import AnalyzeButton from "./components/AnalyzeButton";
import DiagnosisPanel from "./components/DiagnosisPanel";

function App() {
  const [symptom, setSymptom] = useState("");
  const [notes, setNotes] = useState("");

  const [devices, setDevices] = useState([
    {
      id: 1,
      name: "Device 1",
      type: "PC",
    },
    {
      id: 2,
      name: "Device 2",
      type: "Router",
    },
  ]);

  const [connections, setConnections] = useState([
    {
      id: 1,
      from: 1,
      to: 2,
    },
  ]);

  const [commands, setCommands] = useState([
    {
      id: 1,
      command: "",
      output: "",
    },
  ]);

  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // DEVICES
  // -----------------------------

  const addDevice = () => {
    const newDevice = {
      id: Date.now(),
      name: `Device ${devices.length + 1}`,
      type: "PC",
    };

    setDevices((prev) => [...prev, newDevice]);
  };

  const updateDevice = (id, field, value) => {
    setDevices((prev) =>
      prev.map((device) =>
        device.id === id
          ? { ...device, [field]: value }
          : device
      )
    );
  };

  const removeDevice = (id) => {
    setDevices((prev) =>
      prev.filter((device) => device.id !== id)
    );

    setConnections((prev) =>
      prev.filter(
        (connection) =>
          connection.from !== id &&
          connection.to !== id
      )
    );
  };

  // -----------------------------
  // CONNECTIONS
  // -----------------------------

  const addConnection = () => {
    if (devices.length < 2) return;

    setConnections((prev) => [
      ...prev,
      {
        id: Date.now(),
        from: devices[0].id,
        to: devices[1].id,
      },
    ]);
  };

  const updateConnection = (id, field, value) => {
    setConnections((prev) =>
      prev.map((connection) =>
        connection.id === id
          ? {
              ...connection,
              [field]: Number(value),
            }
          : connection
      )
    );
  };

  const removeConnection = (id) => {
    setConnections((prev) =>
      prev.filter(
        (connection) => connection.id !== id
      )
    );
  };

  // -----------------------------
  // COMMANDS
  // -----------------------------

  const addCommand = () => {
    setCommands((prev) => [
      ...prev,
      {
        id: Date.now(),
        command: "",
        output: "",
      },
    ]);
  };

  const updateCommand = (id, field, value) => {
    setCommands((prev) =>
      prev.map((item) =>
        item.id === id
          ? { ...item, [field]: value }
          : item
      )
    );
  };

  const removeCommand = (id) => {
    setCommands((prev) =>
      prev.filter((item) => item.id !== id)
    );
  };

  // -----------------------------
  // ANALYSIS
  // -----------------------------

  const analyzeNetwork = async () => {
    if (!symptom.trim()) {
      alert("Please describe the problem or symptom.");
      return;
    }

    setLoading(true);
    setDiagnosis(null);

    try {
      const payload = {
        symptom,
        devices,
        connections,
        commands,
        notes,
      };

      console.log("Sending payload:", payload);

      const response = await fetch(
        "http://localhost:5000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      const result = await response.json();

      console.log("Backend response:", result);

      if (!response.ok) {
        throw new Error(
          result.error || "Network analysis failed."
        );
      }

      setDiagnosis(result.diagnosis);
    } catch (error) {
      console.error("Analysis error:", error);

      alert(
        error.message ||
          "Unable to connect to the NetSage backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#080b10] text-white">
      <Navbar />

      <main className="mx-auto max-w-7xl px-6 py-10">
        {/* HERO */}

        <section className="mb-10">
          <p className="mb-2 text-sm font-semibold tracking-wider text-sky-400">
            CISCO PACKET TRACER NETWORK TROUBLESHOOTING
          </p>

          <h1 className="text-4xl font-bold tracking-tight">
            Diagnose your network.
          </h1>

          <p className="mt-3 max-w-2xl text-gray-400">
            Provide the symptoms, topology, command
            outputs, and additional notes. NetSage AI will analyze the evidence and recommend the next troubleshooting step.
          </p>
        </section>

        <div className="grid gap-8 lg:grid-cols-[1.35fr_0.85fr]">
          {/* LEFT */}

          <div className="space-y-8">
            <SymptomInput
              value={symptom}
              onChange={setSymptom}
            />

            <TopologyBuilder
              devices={devices}
              connections={connections}
              onAddDevice={addDevice}
              onUpdateDevice={updateDevice}
              onRemoveDevice={removeDevice}
              onAddConnection={addConnection}
              onUpdateConnection={updateConnection}
              onRemoveConnection={removeConnection}
            />

            <CommandOutputs
              commands={commands}
              onAdd={addCommand}
              onUpdate={updateCommand}
              onRemove={removeCommand}
            />

            <NotesInput
              value={notes}
              onChange={setNotes}
            />

            <AnalyzeButton
              loading={loading}
              onClick={analyzeNetwork}
            />
          </div>

          {/* RIGHT */}

          <aside className="lg:sticky lg:top-6 lg:self-start">
            <DiagnosisPanel diagnosis={diagnosis} />
          </aside>
        </div>
      </main>
    </div>
  );
}

export default App;