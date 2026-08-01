import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';

export default function Analytics() {
  const priceTrendData = [
    { month: 'Jan', suv: 12.5, sedan: 8.2, hatchback: 5.4 },
    { month: 'Feb', suv: 12.8, sedan: 8.1, hatchback: 5.5 },
    { month: 'Mar', suv: 12.4, sedan: 7.9, hatchback: 5.2 },
    { month: 'Apr', suv: 13.1, sedan: 8.0, hatchback: 5.1 },
    { month: 'May', suv: 13.5, sedan: 8.3, hatchback: 5.4 },
    { month: 'Jun', suv: 13.2, sedan: 8.1, hatchback: 5.3 },
  ];

  const brandDistribution = [
    { name: 'Maruti Suzuki', count: 45000 },
    { name: 'Hyundai', count: 32000 },
    { name: 'Tata', count: 28000 },
    { name: 'Mahindra', count: 22000 },
    { name: 'Honda', count: 18000 },
    { name: 'Toyota', count: 15000 },
  ];

  return (
    <div className="p-8 h-full overflow-y-auto space-y-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white tracking-tight">Valuation Analytics</h1>
        <p className="text-sm text-slate-400 mt-1">Market trends, price drops, and historical tracking across 10M+ listings.</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        
        {/* Price Trends */}
        <div className="bg-[#141416] border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Average Price Trends (in Lakhs)</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <RechartsLineChart data={priceTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="month" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0A0A0B', borderColor: '#1e293b' }}
                  itemStyle={{ fontSize: '12px' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="suv" name="SUV" stroke="#10b981" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="sedan" name="Sedan" stroke="#6366f1" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="hatchback" name="Hatchback" stroke="#f59e0b" strokeWidth={2} dot={false} />
              </RechartsLineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Brand Distribution */}
        <div className="bg-[#141416] border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Market Share by Brand</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={brandDistribution} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis type="number" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} hide />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{ fill: '#1e293b' }}
                  contentStyle={{ backgroundColor: '#0A0A0B', borderColor: '#1e293b', fontSize: '12px' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      <div className="bg-[#141416] border border-slate-800 rounded-lg p-6">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Depreciation Curves (Sample)</h2>
        <div className="h-64 flex items-center justify-center border border-dashed border-slate-800 rounded bg-[#0D0D0E]">
          <p className="text-slate-500 font-mono text-sm">Requires full historical DB sync (Job #892 pending)</p>
        </div>
      </div>
    </div>
  );
}
