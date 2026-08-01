import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Server, Activity, Database, AlertTriangle, RefreshCw } from "lucide-react";

export default function AdminDashboard() {
  const { data: systemStats, isLoading } = useQuery({
    queryKey: ["admin-stats"],
    queryFn: async () => {
      // Mocking for now since admin endpoints weren't specifically required in earlier backend, but we assume they exist
      return {
        workers_active: 84,
        workers_idle: 16,
        queue_size: 4205,
        error_rate: 0.02,
        marketplaces: [
          { name: "OLX", status: "Healthy", latency: "42ms" },
          { name: "Facebook", status: "Warning", latency: "120ms" },
          { name: "Cars24", status: "Healthy", latency: "38ms" }
        ],
        recent_logs: [
          "[Worker-12] Scraped 45 listings from OLX Delhi",
          "[Worker-45] Timeout on FB Marketplace, retrying...",
          "[Worker-02] Processed 12 price changes"
        ]
      };
    },
  });

  return (
    <div className="p-8 h-full overflow-y-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Scraper Fleet Command</h1>
          <p className="text-sm text-slate-400 mt-1">Manage distributed scraping workers and queues.</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-400 text-white px-4 py-2 rounded text-sm font-medium transition-colors">
          <RefreshCw className="w-4 h-4" />
          Force Sync
        </button>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider">Active Workers</p>
            <Server className="w-4 h-4 text-emerald-500" />
          </div>
          <p className="text-3xl font-light text-white tracking-tight">{systemStats?.workers_active || 0}</p>
        </div>
        
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider">Idle Workers</p>
            <Activity className="w-4 h-4 text-slate-500" />
          </div>
          <p className="text-3xl font-light text-white tracking-tight">{systemStats?.workers_idle || 0}</p>
        </div>

        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider">Queue Size</p>
            <Database className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-3xl font-light text-white tracking-tight">{systemStats?.queue_size?.toLocaleString() || 0}</p>
        </div>

        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider">Global Error Rate</p>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <p className="text-3xl font-light text-white tracking-tight">{(systemStats?.error_rate * 100).toFixed(1)}%</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-[#141416] border border-slate-800 rounded-lg">
          <div className="p-5 border-b border-slate-800">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">Marketplace Health</h2>
          </div>
          <div className="p-5">
            <table className="w-full text-left border-collapse">
              <thead className="text-[10px] text-slate-500 uppercase font-bold border-b border-slate-800">
                <tr>
                  <th className="pb-3">Marketplace</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Avg Latency</th>
                  <th className="pb-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {systemStats?.marketplaces.map((mp: any) => (
                  <tr key={mp.name} className="border-b border-slate-800/50">
                    <td className="py-4 text-white font-medium">{mp.name}</td>
                    <td className="py-4">
                      <span className={`px-2 py-1 rounded text-[10px] font-bold ${mp.status === 'Healthy' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'}`}>
                        {mp.status}
                      </span>
                    </td>
                    <td className="py-4 text-slate-400 font-mono">{mp.latency}</td>
                    <td className="py-4 text-right">
                      <button className="text-[11px] text-indigo-400 hover:text-indigo-300 font-bold uppercase tracking-wider">
                        Restart Jobs
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-[#141416] border border-slate-800 rounded-lg flex flex-col h-[400px]">
          <div className="p-5 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">Live Logs</h2>
            <div className="w-2 h-2 bg-emerald-500 rounded-full shadow-[0_0_8px_#10b981] animate-pulse"></div>
          </div>
          <div className="p-5 flex-1 overflow-y-auto font-mono text-[11px] space-y-3">
            {systemStats?.recent_logs.map((log: string, i: number) => (
              <div key={i} className={`${log.includes('error') || log.includes('Timeout') ? 'text-amber-400' : 'text-slate-400'}`}>
                <span className="text-slate-600 mr-2">{new Date().toLocaleTimeString()}</span>
                {log}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
