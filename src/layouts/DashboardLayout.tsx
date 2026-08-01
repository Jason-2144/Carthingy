import { Outlet, Link, useLocation } from "react-router-dom";
import {
  Search,
  Bell,
  Database,
  Server,
  Archive,
  BarChart,
  LineChart,
  Settings,
  User,
  LogOut
} from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

export default function DashboardLayout() {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Mainframe Dashboard", path: "/dashboard", icon: Database },
    { name: "Search Listings", path: "/search", icon: Search },
    { name: "Scraper Fleet", path: "/admin", icon: Server },
    { name: "Listing Archive", path: "/saved", icon: Archive },
    { name: "Valuation Models", path: "/analytics", icon: BarChart },
    { name: "Price History DB", path: "/alerts", icon: LineChart },
  ];

  return (
    <div className="h-screen w-full bg-[#0A0A0B] text-slate-300 font-sans flex overflow-hidden select-none">
      <aside className="w-64 border-r border-slate-800 flex flex-col bg-[#0D0D0E]">
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-3 h-3 bg-indigo-500 rounded-sm"></div>
            <span className="text-white font-bold tracking-tight text-lg">
              CARSCOPE<span className="text-indigo-500">AI</span>
            </span>
          </div>
          <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">
            Enterprise Infrastructure
          </p>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          <div className="text-[11px] text-slate-600 uppercase font-bold tracking-wider px-2 py-2">
            Engine & Data
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + '/');
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded transition-colors ${
                  isActive
                    ? "text-indigo-400 bg-indigo-500/10 border-l-2 border-indigo-500"
                    : "text-slate-400 hover:bg-slate-800"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="text-sm font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-slate-800 bg-[#0A0A0B]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-slate-800 flex items-center justify-center text-[10px] font-bold text-slate-500 uppercase">
                {user?.full_name?.substring(0, 2) || "US"}
              </div>
              <div>
                <p className="text-xs text-white font-medium">{user?.full_name || "User"}</p>
                <p className="text-[10px] text-slate-500">{user?.is_superuser ? "Admin" : "Analyst"}</p>
              </div>
            </div>
            <button onClick={logout} className="text-slate-500 hover:text-white transition-colors">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>
      <main className="flex-1 flex flex-col">
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-8 bg-[#0D0D0E]">
          <div className="relative w-96">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-slate-500 text-sm">
              <Search className="w-4 h-4" />
            </div>
            <input
              type="text"
              className="w-full bg-[#141416] border border-slate-700 rounded-md py-1.5 pl-10 pr-4 text-sm focus:outline-none focus:border-indigo-500 placeholder-slate-600 font-mono"
              placeholder="SEARCH_IDENTIFIER_OR_VIN"
            />
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-[10px] text-slate-500 uppercase font-bold">
                  Ingestion Rate
                </p>
                <p className="text-xs text-indigo-400 font-mono">1.2k req/s</p>
              </div>
              <div className="h-8 w-px bg-slate-800"></div>
              <div className="text-right">
                <p className="text-[10px] text-slate-500 uppercase font-bold">
                  System Latency
                </p>
                <p className="text-xs text-emerald-400 font-mono">42ms</p>
              </div>
            </div>
            <button className="w-10 h-10 rounded border border-slate-700 flex items-center justify-center hover:bg-slate-800 transition-colors">
              <Bell className="w-4 h-4 text-slate-400" />
            </button>
            <Link to="/profile" className="w-10 h-10 rounded border border-slate-700 flex items-center justify-center hover:bg-slate-800 transition-colors">
              <Settings className="w-4 h-4 text-slate-400" />
            </Link>
          </div>
        </header>
        <section className="flex-1 overflow-hidden relative">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
