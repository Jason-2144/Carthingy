import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Listing } from "../types";
import { ArrowLeft, ExternalLink, MapPin, Calendar, Activity, Info, AlertTriangle, Share2, Heart, TrendingDown } from "lucide-react";
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export default function ListingDetails() {
  const { id } = useParams();

  const { data: listing, isLoading } = useQuery({
    queryKey: ["listing", id],
    queryFn: async () => {
      const res = await api.get(`/listings/${id}`);
      return res.data as Listing;
    },
  });

  if (isLoading) {
    return <div className="p-8 text-slate-500">Loading listing details...</div>;
  }

  if (!listing) {
    return <div className="p-8 text-red-400">Listing not found.</div>;
  }

  // Mock price history if none provided by API
  const historyData = listing.history && listing.history.length > 0 
    ? listing.history.map(h => ({ date: new Date(h.timestamp).toLocaleDateString(), price: h.new_price }))
    : [
        { date: 'First Seen', price: listing.price + (listing.price * 0.05) },
        { date: 'Last Week', price: listing.price + (listing.price * 0.02) },
        { date: 'Current', price: listing.price },
      ];

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0B]">
      {/* Top Bar */}
      <div className="sticky top-0 z-10 bg-[#0D0D0E]/90 backdrop-blur border-b border-slate-800 p-4 px-8 flex items-center justify-between">
        <Link to="/search" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Search
        </Link>
        <div className="flex items-center gap-3">
          <button className="w-9 h-9 rounded border border-slate-700 flex items-center justify-center hover:bg-slate-800 transition-colors text-slate-400">
            <Share2 className="w-4 h-4" />
          </button>
          <button className="w-9 h-9 rounded border border-slate-700 flex items-center justify-center hover:bg-slate-800 transition-colors text-slate-400">
            <Heart className="w-4 h-4" />
          </button>
          <a 
            href={listing.url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-400 text-white px-4 py-2 rounded text-sm font-medium transition-colors"
          >
            View on {listing.marketplace?.name || 'Marketplace'}
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>

      <div className="p-8 max-w-7xl mx-auto space-y-8">
        
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column - Images */}
          <div className="lg:col-span-2 space-y-4">
            <div className="aspect-[16/9] bg-[#141416] rounded-xl border border-slate-800 overflow-hidden relative group">
              {listing.images && listing.images.length > 0 ? (
                <img 
                  src={listing.images[0].image_url} 
                  alt={listing.title} 
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-slate-700">No Image Available</div>
              )}
            </div>
            
            {listing.images && listing.images.length > 1 && (
              <div className="grid grid-cols-4 gap-4">
                {listing.images.slice(1, 5).map((img, i) => (
                  <div key={i} className="aspect-[4/3] bg-[#141416] rounded-lg border border-slate-800 overflow-hidden cursor-pointer hover:border-indigo-500 transition-colors">
                    <img src={img.image_url} alt="" className="w-full h-full object-cover" />
                  </div>
                ))}
              </div>
            )}
            
            {/* Description */}
            <div className="bg-[#141416] rounded-xl border border-slate-800 p-6 mt-8">
              <h3 className="text-white font-bold mb-4 uppercase tracking-wider text-sm">Seller Description</h3>
              <p className="text-slate-400 whitespace-pre-wrap text-sm leading-relaxed">
                {listing.description || "No description provided by the seller."}
              </p>
            </div>
          </div>

          {/* Right Column - Details */}
          <div className="space-y-6">
            
            {/* Core Info Box */}
            <div className="bg-[#141416] rounded-xl border border-slate-800 p-6">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-white mb-2 leading-tight">{listing.title}</h1>
                <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
                  <span className="flex items-center gap-1"><MapPin className="w-3 h-3" /> {listing.registration_city}, {listing.registration_state}</span>
                  <span>•</span>
                  <span>Posted: {new Date(listing.first_seen).toLocaleDateString()}</span>
                  <span>•</span>
                  <span className="font-mono text-indigo-400">{listing.marketplace?.name}</span>
                </div>
              </div>

              <div className="pb-6 border-b border-slate-800">
                <p className="text-[11px] text-slate-500 uppercase font-bold tracking-wider mb-1">Asking Price</p>
                <div className="flex items-end gap-3">
                  <span className="text-4xl font-light text-emerald-400 tracking-tight">
                    ₹{listing.price.toLocaleString()}
                  </span>
                  {listing.market_value && listing.price < listing.market_value && (
                    <span className="bg-emerald-500/10 text-emerald-400 text-xs px-2 py-1 rounded flex items-center gap-1 mb-1 font-medium">
                      <TrendingDown className="w-3 h-3" />
                      ₹{(listing.market_value - listing.price).toLocaleString()} Below Mkt
                    </span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-y-4 pt-6 text-sm">
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Year</p>
                  <p className="text-white font-medium">{listing.registration_year}</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Mileage</p>
                  <p className="text-white font-medium">{listing.km_driven.toLocaleString()} km</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Fuel</p>
                  <p className="text-white font-medium">{listing.fuel}</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Transmission</p>
                  <p className="text-white font-medium">{listing.transmission}</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Ownership</p>
                  <p className="text-white font-medium">{listing.ownership} Owner(s)</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Color</p>
                  <p className="text-white font-medium">{listing.colour || 'N/A'}</p>
                </div>
              </div>
            </div>

            {/* AI Valuation Box (Conceptual) */}
            <div className="bg-indigo-500/5 rounded-xl border border-indigo-500/20 p-6 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
                <Activity className="w-24 h-24 text-indigo-500" />
              </div>
              <h3 className="text-sm font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2 mb-4">
                CarScope Valuation
              </h3>
              
              <div className="space-y-4 relative z-10">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-300">Estimated Market Value</span>
                  <span className="font-mono text-white">₹{(listing.market_value || listing.price * 1.08).toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-300">Deal Score</span>
                  <span className="bg-indigo-500 text-white text-xs font-bold px-2 py-1 rounded">
                    {listing.deal_score || 7.5}/10
                  </span>
                </div>
              </div>
            </div>

            {/* Price History Chart */}
            <div className="bg-[#141416] rounded-xl border border-slate-800 p-6">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Price History</h3>
              <div className="h-48 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsLineChart data={historyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
                    <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(val) => `₹${val/1000}k`} width={45} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0A0A0B', borderColor: '#1e293b', fontSize: '12px' }}
                      itemStyle={{ color: '#10b981' }}
                    />
                    <Line type="stepAfter" dataKey="price" stroke="#10b981" strokeWidth={2} dot={{ r: 3, fill: '#10b981', strokeWidth: 0 }} activeDot={{ r: 5 }} />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
