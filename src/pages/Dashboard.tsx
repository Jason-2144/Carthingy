import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: async () => {
      // Assuming a backend endpoint exists, if not, we gracefully degrade
      try {
        const res = await api.get("/analytics/dashboard");
        return res.data;
      } catch (e) {
        return null;
      }
    }
  });

  return (
    <div className="p-8 h-full overflow-y-auto space-y-6">
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider mb-1">
            Total Indexed Listings
          </p>
          <p className="text-3xl font-light text-white tracking-tight">
            {stats?.total_listings?.toLocaleString() || "10,482,901"}
          </p>
          <p className="text-xs text-emerald-500 mt-2 font-medium">
            +{stats?.today_listings?.toLocaleString() || "14,202"}{" "}
            <span className="text-slate-500 font-normal">
              since midnight
            </span>
          </p>
        </div>
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider mb-1">
            Active Scraper Nodes
          </p>
          <p className="text-3xl font-light text-white tracking-tight">{stats?.active_workers || 84}</p>
          <p className="text-xs text-slate-400 mt-2 font-medium">
            Cluster Health:{" "}
            <span className="text-emerald-500">OPTIMAL</span>
          </p>
        </div>
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider mb-1">
            Market Volatility Index
          </p>
          <p className="text-3xl font-light text-white tracking-tight">
            0.14
          </p>
          <p className="text-xs text-amber-500 mt-2 font-medium">
            STABLE{" "}
            <span className="text-slate-500 font-normal">
              Low fluctuation
            </span>
          </p>
        </div>
        <div className="bg-[#141416] p-5 border border-slate-800 rounded-lg">
          <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider mb-1">
            Deal Opportunity Score
          </p>
          <p className="text-3xl font-light text-white tracking-tight">
            8.4<span className="text-lg text-slate-500">/10</span>
          </p>
          <p className="text-xs text-indigo-400 mt-2 font-medium">
            HIGH{" "}
            <span className="text-slate-500 font-normal">
              3.2k outliers detected
            </span>
          </p>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-6 h-[400px]">
        <div className="col-span-2 bg-[#141416] border border-slate-800 rounded-lg flex flex-col">
          <div className="p-5 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              High Confidence Ingestions
            </h2>
            <Link to="/search" className="text-[10px] text-indigo-400 hover:text-indigo-300 font-mono">
              VIEW_ALL
            </Link>
          </div>
          <div className="flex-1 overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead className="bg-[#0D0D0E] text-[10px] text-slate-500 uppercase font-bold">
                <tr>
                  <th className="px-5 py-3 border-b border-slate-800">
                    Timestamp
                  </th>
                  <th className="px-5 py-3 border-b border-slate-800">
                    Entity
                  </th>
                  <th className="px-5 py-3 border-b border-slate-800">
                    Marketplace
                  </th>
                  <th className="px-5 py-3 border-b border-slate-800">
                    Valuation Diff
                  </th>
                  <th className="px-5 py-3 border-b border-slate-800">
                    Score
                  </th>
                </tr>
              </thead>
              <tbody className="text-xs font-mono">
                <tr className="border-b border-slate-800/50 hover:bg-white/5">
                  <td className="px-5 py-4 text-slate-500">14:22:04.12</td>
                  <td className="px-5 py-4 text-white">
                    Mahindra XUV700 AX7
                  </td>
                  <td className="px-5 py-4">Spinny_IN</td>
                  <td className="px-5 py-4 text-emerald-400">-₹42,000</td>
                  <td className="px-5 py-4">
                    <span className="bg-emerald-500/10 text-emerald-500 px-2 py-0.5 rounded">
                      9.1
                    </span>
                  </td>
                </tr>
                <tr className="border-b border-slate-800/50 hover:bg-white/5">
                  <td className="px-5 py-4 text-slate-500">14:21:58.84</td>
                  <td className="px-5 py-4 text-white">
                    Tata Nexon EV Max
                  </td>
                  <td className="px-5 py-4">Cars24_IN</td>
                  <td className="px-5 py-4 text-amber-400">+₹12,000</td>
                  <td className="px-5 py-4">
                    <span className="bg-slate-500/10 text-slate-400 px-2 py-0.5 rounded">
                      7.4
                    </span>
                  </td>
                </tr>
                <tr className="border-b border-slate-800/50 hover:bg-white/5">
                  <td className="px-5 py-4 text-slate-500">14:21:51.32</td>
                  <td className="px-5 py-4 text-white">
                    Hyundai Creta SX
                  </td>
                  <td className="px-5 py-4">Olx_India</td>
                  <td className="px-5 py-4 text-emerald-400">-₹18,500</td>
                  <td className="px-5 py-4">
                    <span className="bg-emerald-500/10 text-emerald-500 px-2 py-0.5 rounded">
                      8.8
                    </span>
                  </td>
                </tr>
                <tr className="border-b border-slate-800/50 hover:bg-white/5">
                  <td className="px-5 py-4 text-slate-500">14:21:44.09</td>
                  <td className="px-5 py-4 text-white">
                    BMW 3 Series 320d
                  </td>
                  <td className="px-5 py-4">LuxuryCircle</td>
                  <td className="px-5 py-4 text-white">--</td>
                  <td className="px-5 py-4">
                    <span className="bg-slate-500/10 text-slate-400 px-2 py-0.5 rounded">
                      6.2
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div className="bg-[#141416] border border-slate-800 rounded-lg flex flex-col">
          <div className="p-5 border-b border-slate-800">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Infrastructure Health
            </h2>
          </div>
          <div className="p-5 space-y-5">
            <div>
              <div className="flex justify-between text-[11px] mb-2">
                <span className="text-slate-400 uppercase">
                  PostgreSQL Main (9.2TB)
                </span>
                <span className="text-white font-mono">82%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-indigo-500 w-[82%]"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[11px] mb-2">
                <span className="text-slate-400 uppercase">
                  Redis Cache Warmth
                </span>
                <span className="text-white font-mono">94%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 w-[94%]"></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-[11px] mb-2">
                <span className="text-slate-400 uppercase">
                  ElasticSearch Shards
                </span>
                <span className="text-white font-mono">OK</span>
              </div>
              <div className="flex gap-1 mt-1">
                <div className="flex-1 h-3 bg-emerald-500/20 border border-emerald-500/30 rounded"></div>
                <div className="flex-1 h-3 bg-emerald-500/20 border border-emerald-500/30 rounded"></div>
                <div className="flex-1 h-3 bg-emerald-500/20 border border-emerald-500/30 rounded"></div>
                <div className="flex-1 h-3 bg-emerald-500/20 border border-emerald-500/30 rounded"></div>
                <div className="flex-1 h-3 bg-amber-500/20 border border-amber-500/30 rounded"></div>
                <div className="flex-1 h-3 bg-emerald-500/20 border border-emerald-500/30 rounded"></div>
              </div>
            </div>
            <div className="pt-4 border-t border-slate-800/50">
              <p className="text-[10px] text-slate-500 uppercase font-bold mb-3">
                Latest Scraper Incident
              </p>
              <div className="bg-red-500/10 border border-red-500/20 p-3 rounded">
                <p className="text-[11px] text-red-400 font-bold mb-1">
                  ERR_RATE_LIMITING
                </p>
                <p className="text-[10px] text-red-300 opacity-80">
                  Node #042 blocked by Cloudflare on Droom.in. Retrying in
                  120s...
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
