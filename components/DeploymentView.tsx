
import React from 'react';
import { Package, Terminal, Box, ArrowRight, CheckCircle2, FileCode, Play, AlertCircle, Info, ShieldAlert, Cpu } from 'lucide-react';

const DeploymentView: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-in fade-in duration-500 pb-20">
      <div className="space-y-4 text-center py-8">
        <h2 className="text-3xl font-black text-white">Desktop Distribution Center</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          v1.7.0 - Optimized for Windows 10/11 Production Environments.
        </p>
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
              <Terminal className="w-3 h-3" /> Python Not Found?
            </h4>
            <p className="text-[11px] text-slate-500 mb-3">If 'python' fails, we use 'py' (Windows Launcher). Install/Repair Python via Microsoft Store if both fail.</p>
            <div className="bg-slate-950 p-2 rounded font-mono text-[10px] text-emerald-400">
              py -m pip install -r backend/requirements.txt
            </div>
          </div>
          
          <div className="bg-slate-950/50 p-4 rounded-xl border border-red-500/10">
            <h4 className="text-xs font-bold text-slate-300 uppercase mb-2 flex items-center gap-2">
              <Cpu className="w-3 h-3" /> Vite Build Error?
            </h4>
            <p className="text-[11px] text-slate-500 mb-3">If build fails due to missing modules, force a clean reinstall of dependencies.</p>
            <div className="bg-slate-950 p-2 rounded font-mono text-[10px] text-blue-400">
              npm install --force
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
          <h4 className="font-bold text-amber-200">Step 0: Prepare Python via Launcher</h4>
          <p className="text-sm text-amber-500/80 leading-relaxed">
            Run this command to install requirements using the Windows Python Launcher:
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
            Generate <span className="text-indigo-400 font-bold">hub_core.exe</span>. Now using <span className="font-mono">py -m PyInstaller</span> for stability.
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
            Build the Electron app using the fixed React/Vite pipeline.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-blue-400">
            npm run dist:ui
          </div>
        </div>
      </div>

      {/* Final Build Call to Action */}
      <div className="bg-gradient-to-br from-indigo-900/20 to-slate-900 border border-indigo-500/20 rounded-3xl p-10 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-2 text-center md:text-left">
          <h3 className="text-2xl font-bold text-white">YeiciCap Hub Build Cycle</h3>
          <p className="text-slate-400 text-sm">Full automated compilation for distribution.</p>
        </div>
        <button className="flex items-center gap-3 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-black transition-all shadow-xl shadow-indigo-600/20 active:scale-95 group">
          <Play className="w-5 h-5 fill-current" />
          COMPILE STANDALONE
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default DeploymentView;
