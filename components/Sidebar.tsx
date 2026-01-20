
import React from 'react';
import { LayoutDashboard, Zap, Settings, ShieldQuestion, Package } from 'lucide-react';

interface SidebarProps {
  activeTab: 'dashboard' | 'architecture' | 'settings' | 'deployment';
  setActiveTab: (tab: 'dashboard' | 'architecture' | 'settings' | 'deployment') => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'architecture', icon: Zap, label: 'Architecture' },
    { id: 'deployment', icon: Package, label: 'Deployment' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ] as const;

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/40 flex flex-col">
      <div className="p-6">
        <div className="flex flex-col gap-6">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                activeTab === item.id 
                ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-600/20' 
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <item.icon className={`w-5 h-5 transition-transform duration-200 ${activeTab === item.id ? 'scale-110' : 'group-hover:scale-110'}`} />
              <span className="font-semibold text-sm">{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-auto p-6">
        <div className="p-4 rounded-xl bg-slate-800/30 border border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <Package className="w-4 h-4 text-indigo-400" />
            <span className="text-xs font-bold text-slate-300">Ready for Build?</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Run 'npm run dist' to generate the YeiciCap_Hub.exe installer.
          </p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
