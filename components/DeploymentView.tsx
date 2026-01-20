
import React from 'react';
import { Package, Terminal, Box, ArrowRight, CheckCircle2, FileCode, Play, AlertCircle, Info } from 'lucide-react';

const DeploymentView: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-10 animate-in fade-in duration-500 pb-20">
      <div className="space-y-4 text-center py-8">
        <h2 className="text-3xl font-black text-white">Desktop Distribution Center</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Transform the development bridge into a professional, standalone Windows application.
        </p>
      </div>

      {/* Step 0: Critical Environment Setup */}
      <div className="bg-amber-500/10 border border-amber-500/20 rounded-3xl p-6 flex items-start gap-4">
        <div className="p-2 bg-amber-500/20 rounded-lg">
          <AlertCircle className="w-6 h-6 text-amber-500" />
        </div>
        <div className="space-y-1">
          <h4 className="font-bold text-amber-200">Step 0: Prepare Python Environment</h4>
          <p className="text-sm text-amber-500/80 leading-relaxed">
            Before building, ensure you have installed the core requirements. Run this in your terminal:
          </p>
          <div className="mt-2 bg-slate-950 p-3 rounded-xl border border-amber-500/10 font-mono text-xs text-amber-400">
            pip install -r backend/requirements.txt
          </div>
        </div>
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
            Convert the Python logic into <span className="text-indigo-400 font-bold">hub_core.exe</span> using PyInstaller.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-indigo-400">
            npm run dist:backend
          </div>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Uses 'python -m PyInstaller' (Safe Mode)
            </li>
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Standalone Binary Generation
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
            Bundle the React interface into a professional Electron window.
          </p>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-blue-400">
            npm run dist:ui
          </div>
          <ul className="space-y-2">
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Native Windows Installer (.exe)
            </li>
            <li className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Hardware Acceleration Active
            </li>
          </ul>
        </div>
      </div>

      {/* Final Build Call to Action */}
      <div className="bg-gradient-to-br from-indigo-900/20 to-slate-900 border border-indigo-500/20 rounded-3xl p-10 flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-2">
          <h3 className="text-2xl font-bold text-white">Full Build Cycle</h3>
          <p className="text-slate-400 text-sm italic">Generates the complete installer in a single pass.</p>
        </div>
        <button className="flex items-center gap-3 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-black transition-all shadow-xl shadow-indigo-600/20 active:scale-95 group">
          <Play className="w-5 h-5 fill-current" />
          RUN npm run dist
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>

      <div className="flex items-center justify-center gap-2 text-slate-600">
        <Info className="w-3 h-3" />
        <span className="text-[10px] font-bold uppercase tracking-[0.2em]">
          Logs available in /dist directory after completion
        </span>
      </div>
    </div>
  );
};

export default DeploymentView;
