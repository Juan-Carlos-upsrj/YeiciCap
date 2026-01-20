
import React from 'react';
import { 
  Zap, 
  Activity, 
  Target, 
  Box, 
  Share2, 
  CheckCircle2, 
  RefreshCcw,
  ArrowRight
} from 'lucide-react';
import { StreamMetrics, DestinationNode, ConnectionStatus } from '../types';

interface DashboardProps {
  metrics: StreamMetrics;
}

const DESTINATIONS: DestinationNode[] = [
  { id: '1', name: 'Unreal Engine 5.4 (Workstation)', protocol: 'UDP', address: '127.0.0.1', port: 8888, status: ConnectionStatus.CONNECTED, activeSkeletons: 2 },
  { id: '2', name: 'Maya 2024 Node', protocol: 'UDP', address: '192.168.1.42', port: 7001, status: ConnectionStatus.CONNECTED, activeSkeletons: 1 },
  { id: '3', name: 'WebSockets Bridge', protocol: 'Websocket', address: '0.0.0.0', port: 3000, status: ConnectionStatus.CONNECTED, activeSkeletons: 3 },
  { id: '4', name: 'Python Analytics', protocol: 'TCP', address: '127.0.0.1', port: 9999, status: ConnectionStatus.DISCONNECTED, activeSkeletons: 0 },
];

const Dashboard: React.FC<DashboardProps> = ({ metrics }) => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard 
          label="Stream Frequency" 
          value={`${metrics.fps.toFixed(1)} Hz`} 
          icon={Activity} 
          color="text-indigo-400" 
          sub="Synchronized with Motive Clock"
        />
        <MetricCard 
          label="Network Latency" 
          value={`${metrics.latency.toFixed(2)} ms`} 
          icon={Zap} 
          color="text-emerald-400" 
          sub="Jitter: < 0.1ms"
        />
        <MetricCard 
          label="Packet Flux" 
          value={metrics.packetsPerSecond.toString()} 
          icon={Target} 
          color="text-blue-400" 
          sub="Payload: 2.4 MB/s"
        />
        <MetricCard 
          label="Error Rate" 
          value={`${metrics.droppedPackets}`} 
          icon={RefreshCcw} 
          color="text-orange-400" 
          sub="Packet Loss: 0.001%"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Active Nodes List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold flex items-center gap-2">
              <Share2 className="w-5 h-5 text-indigo-400" />
              Distribution Nodes
            </h2>
            <button className="text-xs font-bold text-indigo-400 hover:text-indigo-300">ADD NODE +</button>
          </div>
          
          <div className="grid gap-3">
            {DESTINATIONS.map(node => (
              <div 
                key={node.id} 
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between hover:border-slate-700 transition-all group"
              >
                <div className="flex items-center gap-4">
                  <div className={`p-2 rounded-lg ${node.status === ConnectionStatus.CONNECTED ? 'bg-emerald-500/10' : 'bg-slate-800'}`}>
                    <Box className={`w-5 h-5 ${node.status === ConnectionStatus.CONNECTED ? 'text-emerald-400' : 'text-slate-500'}`} />
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-200">{node.name}</h3>
                    <p className="text-xs text-slate-500 font-mono">{node.protocol} | {node.address}:{node.port}</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-slate-500 uppercase">Skeletons</p>
                    <p className="text-sm font-bold text-indigo-400">{node.activeSkeletons}</p>
                  </div>
                  <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/50 border border-slate-700">
                    <div className={`w-1.5 h-1.5 rounded-full ${node.status === ConnectionStatus.CONNECTED ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'}`} />
                    <span className={`text-[10px] font-bold ${node.status === ConnectionStatus.CONNECTED ? 'text-emerald-400' : 'text-slate-500'}`}>
                      {node.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Skeleton Monitor */}
        <div className="space-y-4">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <Box className="w-5 h-5 text-indigo-400" />
            Detected Skeletons
          </h2>
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 aspect-square flex flex-col items-center justify-center relative overflow-hidden">
            {/* Visualizer Mockup */}
            <div className="absolute inset-0 opacity-10">
              <div className="w-full h-full grid grid-cols-10 grid-rows-10">
                {Array.from({ length: 100 }).map((_, i) => (
                  <div key={i} className="border border-indigo-500/20" />
                ))}
              </div>
            </div>
            
            <div className="z-10 text-center">
              <div className="relative w-32 h-32 mx-auto mb-4">
                <div className="absolute inset-0 border-2 border-indigo-500/30 rounded-full animate-ping duration-[3s]" />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Activity className="w-12 h-12 text-indigo-500" />
                </div>
              </div>
              <h3 className="font-bold text-slate-200">2 Active Subjects</h3>
              <p className="text-xs text-slate-500 mt-2 font-mono uppercase tracking-widest">Tracking Stable</p>
            </div>

            <div className="w-full mt-6 space-y-2">
              <SkeletonItem name="Subject_Alpha" bones={21} markers={42} />
              <SkeletonItem name="Subject_Beta" bones={21} markers={38} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, icon: Icon, color, sub }: any) => (
  <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl hover:border-indigo-500/50 transition-all duration-300">
    <div className="flex justify-between items-start mb-4">
      <div className={`p-2.5 rounded-xl bg-slate-800/50 ${color}`}>
        <Icon className="w-5 h-5" />
      </div>
      <span className="text-[10px] font-bold text-slate-600 bg-slate-800 px-2 py-0.5 rounded">LIVE</span>
    </div>
    <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">{label}</p>
    <h3 className={`text-2xl font-bold ${color}`}>{value}</h3>
    <p className="text-[10px] text-slate-600 mt-2 font-medium">{sub}</p>
  </div>
);

const SkeletonItem = ({ name, bones, markers }: any) => (
  <div className="flex items-center justify-between p-2 rounded-lg bg-slate-800/30 border border-slate-700/30">
    <span className="text-xs font-bold text-slate-400">{name}</span>
    <div className="flex gap-3">
      <span className="text-[10px] text-slate-500 font-mono">B:{bones}</span>
      <span className="text-[10px] text-slate-500 font-mono">M:{markers}</span>
    </div>
  </div>
);

export default Dashboard;
