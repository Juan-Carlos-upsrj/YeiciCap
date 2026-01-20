
import React from 'react';
import { 
  Network, 
  Cpu, 
  Layers, 
  ChevronRight, 
  Code2, 
  Database, 
  Zap, 
  Settings2,
  Lock
} from 'lucide-react';

const ArchDetails: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto space-y-12 animate-in fade-in duration-700">
      <div className="space-y-4">
        <h2 className="text-3xl font-black tracking-tight text-white flex items-center gap-4">
          <Layers className="text-indigo-500 w-8 h-8" />
          Technical Architecture Guide
        </h2>
        <p className="text-slate-400 text-lg leading-relaxed max-w-3xl">
          YeiciCap Hub is designed as a zero-copy, multi-threaded bridge system optimized for 
          ultra-low latency MoCap data processing and distribution.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <ArchColumn 
          title="1. Core Engine" 
          icon={Cpu}
          description="High-frequency data ingestion and processing."
          items={[
            "NatNet SDK 4.1 C++ Implementation",
            "Multi-threaded Packet Parsing",
            "Zero-Latency Buffering System",
            "Timecode Synchronization (SMPTE)"
          ]}
        />
        <ArchColumn 
          title="2. Distribution Layer" 
          icon={Network}
          description="Efficient protocol-based streaming."
          items={[
            "UDP Unicast/Multicast Support",
            "WebSocket Real-time Bridge",
            "Variable Precision Compression",
            "Client Handshake Protocol"
          ]}
        />
        <ArchColumn 
          title="3. User Control" 
          icon={Settings2}
          description="Monitoring and configuration interface."
          items={[
            "React/TS Monitoring Dashboard",
            "Remote Telemetry API",
            "Dynamic Bone Remapping",
            "Visual Frame Diagnostics"
          ]}
        />
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-8">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-indigo-600 rounded-2xl shadow-lg shadow-indigo-600/20">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Recommended Technology Stack</h3>
            <p className="text-slate-400 text-sm">For optimal MVP implementation</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-1 bg-indigo-600 rounded-full" />
              <div className="space-y-2">
                <h4 className="font-bold text-slate-200">Backend: C++ / Rust</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  C++ is mandatory for utilizing the <strong>NatNet SDK</strong> natively. 
                  Using modern C++ (C++20) ensures memory safety and high performance. 
                  For the bridge logic, <strong>Rust</strong> is a great alternative if 
                  building custom packet parsers due to its superior concurrency model.
                </p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="w-1 bg-blue-500 rounded-full" />
              <div className="space-y-2">
                <h4 className="font-bold text-slate-200">Network: ASIO / ZeroMQ</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  Use <strong>Boost.ASIO</strong> or <strong>standalone ASIO</strong> for non-blocking 
                  asynchronous network I/O. For high-reliability data streams to 
                  multiple local clients, <strong>UDP Multicast</strong> is the industry standard.
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-1 bg-emerald-500 rounded-full" />
              <div className="space-y-2">
                <h4 className="font-bold text-slate-200">Frontend: React + Vite + Tailwind</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  For the hub management interface, React provides a reactive way 
                  to display high-frequency metrics. Use <strong>WebSockets</strong> to stream 
                  heartbeat data from the C++ core to the UI.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="w-1 bg-orange-500 rounded-full" />
              <div className="space-y-2">
                <h4 className="font-bold text-slate-200">Protocols: FlatBuffers</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  Instead of JSON, use <strong>Google FlatBuffers</strong> for skeletal data serialization. 
                  It allows reading data without an explicit parsing/unpacking step, 
                  saving critical microseconds.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ArchColumn = ({ title, icon: Icon, description, items }: any) => (
  <div className="space-y-6">
    <div className="flex items-center gap-3">
      <div className="p-2 rounded-lg bg-slate-800 border border-slate-700">
        <Icon className="w-5 h-5 text-indigo-400" />
      </div>
      <h3 className="font-bold text-white uppercase text-sm tracking-widest">{title}</h3>
    </div>
    <p className="text-slate-500 text-sm leading-snug">{description}</p>
    <ul className="space-y-3">
      {items.map((item: string, idx: number) => (
        <li key={idx} className="flex items-center gap-3 text-slate-300 group">
          <ChevronRight className="w-4 h-4 text-indigo-500 group-hover:translate-x-1 transition-transform" />
          <span className="text-sm font-medium">{item}</span>
        </li>
      ))}
    </ul>
  </div>
);

export default ArchDetails;
