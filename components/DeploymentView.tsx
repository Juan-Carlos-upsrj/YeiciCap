
import React from 'react';
import { Package, Terminal, Box, ArrowRight, CheckCircle2, FileCode, Play, AlertCircle, Info, ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';

const DeploymentView: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-in fade-in duration-500 pb-20">
      <div className="space-y-4 text-center py-8">
        <h2 className="text-3xl font-black text-white">Desktop Distribution Center</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          v1.8.0 - Lean build pipeline. Optimized for stability and zero-compiler installation.
        </p>
      </div>

      {/* Critical Python Version Warning */}
      <div className="bg-orange-500/10 border border-orange-500/20 rounded-3xl p-6 space-y-4">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-6 h-6 text-orange-500" />
          <h3 className="text-lg font-bold text-orange-200">Python Compatibility Note</h3>
        </div>
        <p className="text-sm text-slate-400 leading-relaxed">
          It looks like you might be using a <span className="text-orange-400 font-bold">Preview version of Python (3.14+)</span>. 
          Scientific packages often fail to build on preview versions because pre-compiled binaries (wheels) are not yet available.
        </p>
        <div className="bg-slate-950 p-4 rounded-xl border border-orange-500/10">
          <p className="text-xs text-slate-300 font-bold uppercase mb-2">Recommended Setup:</p>
          <ul className="text-xs text-slate-500 space-y-1 list-disc list-inside">
            <li>Use <span className="text-emerald-400">Python 3.11</span> or <span className="text-emerald-400">3.12</span> for the most stable experience.</li>
            <li>We have removed <span className="font-mono">scipy</span> to unblock your current build.</li>
          </ul>
        </div>
      </div>

      {/* Troubleshooting Section */}
      <div className="bg-red-500/10 border border-red-500/20 rounded-3xl p-6 space-y-4">
        <div className="flex items-center gap-3">
          <ShieldAlert className="w-6 h-6 text-red-500" />
          <h3 className="text-lg font-bold text-red-200">Common Windows Fixes</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-950/50 p-4 rounded-xl border border-red-500/10">
            <h4 className="text-xs font-bold text-slate-300 uppercase mb-2 flex items-center gap-2">
              <Terminal className="w-3 h-3" /> Still failing?
            </h4>
            <p className="text-[11px] text-slate-500 mb-3">Try upgrading pip before installing requirements:</p>
            <div className="bg-slate-950 p-2 rounded font-mono text-[10px] text-emerald-400">
              py -m pip install --upgrade pip
            </div>
          </div>
          
          <div className="bg-slate-950/50 p-4 rounded-xl border border-red-500/10">
            <h4 className="text-xs font-bold text-slate-300 uppercase mb-2 flex items-center gap-2">
              <Cpu className="w-3 h-3" /> Force Install
            </h4>
            <p className="text-[11px] text-slate-500 mb-3">If libraries conflict, try a clean force install:</p>
            <div className="bg-slate-950 p-2 rounded font-mono text-[10px] text-blue-400">
              py -m pip install --force-reinstall -r backend/requirements.txt
            </div>
          </div>
        </div>
      </div>

      {/* Step 0: Critical Environment Setup */}
      <div className="bg-amber-500/10 border border-amber-500/20 rounded-3xl p-6 flex items-start gap-4">
        <div className="p-2 bg-amber-500/20 rounded-lg">
          <AlertCircle className="w-6 h-6 text-amber-500" />
        </div>
        <div className="space-y-1">
          <h4 className="font-bold text-amber-200">Step 0: Prepare Python Environment</h4>
          <p className="text-sm text-amber-500/80 leading-relaxed">
            Run this command (updated for v1.8.0):
          </p>
          <div className="mt-2 bg-slate-950 p-3 rounded-xl border border-amber-500/10 font-mono text-xs text-amber-400">
            py -m pip install -r backend/requirements.txt
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <Box className="w-24 h-24 text-white" />
          </div>
          <div className="flex items-center gap-3">
            <div className="bg-indigo-500 p-2 rounded-lg">
              <Terminal className="w-5 h-5 text-white" />
            </div>
            <h3 className="font-bold text-lg">1. Freeze Core Engine</h3>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            Generate <span className="text-indigo-400 font-bold">hub_core.exe</span>. Optimized backend without heavy scientific overhead.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-indigo-400">
            npm run dist:backend
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <FileCode className="w-24 h-24 text-white" />
          </div>
          <div className="flex items-center gap-3">
            <div className="bg-blue-500 p-2 rounded-lg">
              <Package className="w-5 h-5 text-white" />
            </div>
            <h3 className="font-bold text-lg">2. Package Desktop UI</h3>
          </div>
          <p className="text-sm text-slate-400 leading-relaxed">
            Build the Electron app using the production-ready React/Vite pipeline.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-blue-400">
            npm run dist:ui
          </div>
        </div>
      </div>

      {/* Final Build Call to Action */}
      <div className="bg-gradient-to-br from-indigo-900/20 to-slate-900 border border-indigo-500/20 rounded-3xl p-10 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-2 text-center md:text-left">
          <h3 className="text-2xl font-bold text-white">Ready for Distribution</h3>
          <p className="text-slate-400 text-sm">Standalone installer generation for YeiciCap Hub.</p>
        </div>
        <button className="flex items-center gap-3 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-black transition-all shadow-xl shadow-indigo-600/20 active:scale-95 group">
          <Play className="w-5 h-5 fill-current" />
          BUILD PRODUCTION EXE
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default DeploymentView;
