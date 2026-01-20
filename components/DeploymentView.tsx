
import React from 'react';
import { Package, Terminal, Box, ArrowRight, CheckCircle2, FileCode, Play } from 'lucide-react';

const DeploymentView: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-in fade-in duration-500">
      <div className="space-y-4 text-center py-8">
        <h2 className="text-3xl font-black text-white">Desktop Distribution Center</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Transform the development bridge into a professional, standalone Windows application.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Step 1: Backend Freeze */}
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
            Convert the Python logic (NatNet & Numpy) into a single optimized executable 
            that handles the real-time mathematics.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-indigo-400">
            npm run dist:backend
          </div>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Bundles Numpy & Math libraries
            </li>
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Standalone EXE (hub_core.exe)
            </li>
          </ul>
        </div>

        {/* Step 2: UI Packaging */}
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
            Bundle the React interface into a professional Electron window with 
            system tray support and native performance.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-blue-400">
            npm run dist:ui
          </div>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Hardware Acceleration
            </li>
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Multi-window support
            </li>
          </ul>
        </div>
      </div>

      {/* Final Build Call to Action */}
      <div className="bg-gradient-to-br from-indigo-900/20 to-slate-900 border border-indigo-500/20 rounded-3xl p-10 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-2">
          <h3 className="text-2xl font-bold text-white">Ready for Production?</h3>
          <p className="text-slate-400">Run the master build command to generate the final installer.</p>
        </div>
        <button className="flex items-center gap-3 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-black transition-all shadow-xl shadow-indigo-600/20 active:scale-95 group">
          <Play className="w-5 h-5 fill-current" />
          GENERATE INSTALLER (.msi)
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>

      <div className="text-center">
        <span className="text-[10px] font-bold text-slate-600 uppercase tracking-[0.2em]">
          Target Architecture: Windows x64 (10/11)
        </span>
      </div>
    </div>
  );
};

export default DeploymentView;
