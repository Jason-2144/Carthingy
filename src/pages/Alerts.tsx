import { Bell, Plus, Settings } from "lucide-react";

export default function Alerts() {
  const alerts = [
    { id: 1, name: "XUV700 Price Drop", criteria: "Mahindra XUV700 < ₹18L", status: "Active", hits: 12 },
    { id: 2, name: "New Creta Automatics", criteria: "Hyundai Creta • Auto • 2022+", status: "Active", hits: 45 },
    { id: 3, name: "High Score Deals", criteria: "Any • Deal Score > 8.5", status: "Paused", hits: 0 },
  ];

  return (
    <div className="p-8 h-full flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Market Alerts</h1>
          <p className="text-sm text-slate-400 mt-1">Automated notifications for price drops and new listings.</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-400 text-white px-4 py-2 rounded text-sm font-medium transition-colors">
          <Plus className="w-4 h-4" />
          Create Alert
        </button>
      </div>

      <div className="bg-[#141416] border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead className="bg-[#0D0D0E] text-[10px] text-slate-500 uppercase font-bold">
            <tr>
              <th className="px-6 py-4 border-b border-slate-800">Alert Name</th>
              <th className="px-6 py-4 border-b border-slate-800">Match Criteria</th>
              <th className="px-6 py-4 border-b border-slate-800">Status</th>
              <th className="px-6 py-4 border-b border-slate-800">Recent Hits</th>
              <th className="px-6 py-4 border-b border-slate-800 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {alerts.map((alert) => (
              <tr key={alert.id} className="border-b border-slate-800/50 hover:bg-white/5">
                <td className="px-6 py-4 text-white font-medium flex items-center gap-3">
                  <Bell className={`w-4 h-4 ${alert.status === 'Active' ? 'text-indigo-500' : 'text-slate-500'}`} />
                  {alert.name}
                </td>
                <td className="px-6 py-4 text-slate-400">{alert.criteria}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${alert.status === 'Active' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-slate-800 text-slate-400'}`}>
                    {alert.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-white">{alert.hits}</td>
                <td className="px-6 py-4 text-right">
                  <button className="text-slate-400 hover:text-white transition-colors p-2">
                    <Settings className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
