
import React, { useState, useEffect, useCallback } from 'react';
import { 
  Activity, 
  Settings, 
  Share2, 
  Cpu, 
  Network,
  Zap,
  Terminal,
  Calculator,
  ShieldCheck
} from 'lucide-react';
import { ConnectionStatus, StreamMetrics } from './types';
import Dashboard from './components/Dashboard';
import ArchDetails from './components/ArchDetails';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'architecture' | 'settings'>('dashboard');
  const [metrics, setMetrics] = useState<StreamMetrics>({
    fps: 120,
    latency: 0.95,
    packetsPerSecond: 1450,
    droppedPackets: 0
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        fps: 119.98 + Math.random() * 0.04,
        latency: 0.75 + Math.random() * 0.1,
        packetsPerSecond: 1450 + Math.floor(Math.random() * 2),
      }));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen w-screen bg-slate-950 font-sans text-slate-200">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-900/50 backdrop-blur-md sticky top-0 z-20">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-600 p-2 rounded-lg shadow-lg shadow-indigo-600/20">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-lg font-black tracking-tighter bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent leading-none">
                YEICICAP HUB
              </h1>
              <span className="text-[10px] font-mono text-indigo-400 font-bold tracking-widest">v1.4.0-STABLE</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Diagnostic: Active</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[10px] font-black text-emerald-400 uppercase tracking-widest">Core: Distributing</span>
            </div>
            <button className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors border border-transparent hover:border-slate-700">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto bg-slate-950 p-6 custom-scrollbar">
          {activeTab === 'dashboard' && <Dashboard metrics={metrics} />}
          {activeTab === 'architecture' && <ArchDetails />}
          {activeTab === 'settings' && (
            <div className="max-w-4xl mx-auto py-12 text-center">
              <Terminal className="w-16 h-16 mx-auto mb-4 text-slate-700" />
              <h3 className="text-xl font-bold text-slate-200">System Integration Console</h3>
              <p className="text-slate-500 mt-2">Active TCP Server on Port 54321. JSON Streaming Protocol.</p>
            </div>
          )}
        </div>

        <footer className="h-8 border-t border-slate-800 bg-slate-900 px-6 flex items-center justify-between text-[10px] text-slate-500 uppercase tracking-widest font-bold">
          <div className="flex gap-6">
            <span className="flex items-center gap-1.5">
              <Network className="w-3 h-3 text-indigo-500" /> EXPORTER ACTIVE
            </span>
            <span className="flex items-center gap-1.5 font-mono text-indigo-400">
              PORT: 54321
            </span>
          </div>
          <div className="flex gap-6 items-center">
            <span className="text-indigo-400 uppercase tracking-widest">Pipeline: Optimized</span>
            <div className="w-px h-3 bg-slate-800" />
            <span className="text-emerald-400">READY FOR DCC</span>
          </div>
        </footer>
      </main>
    </div>
  );
};

export default App;
