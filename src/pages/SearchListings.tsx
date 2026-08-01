import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Listing } from "../types";
import { Link } from "react-router-dom";
import { Search, Filter, SlidersHorizontal, Map, Grid, List } from "lucide-react";

export default function SearchListings() {
  const [search, setSearch] = useState("");
  const [view, setView] = useState<"grid" | "list">("grid");

  const { data: listings, isLoading } = useQuery({
    queryKey: ["listings", search],
    queryFn: async () => {
      const res = await api.get(`/listings?query=${search}&limit=20`);
      return res.data as Listing[];
    },
  });

  return (
    <div className="h-full flex flex-col">
      {/* Search Header */}
      <div className="border-b border-slate-800 p-6 bg-[#141416]">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-slate-500">
              <Search className="w-5 h-5" />
            </div>
            <input
              type="text"
              className="w-full bg-[#0D0D0E] border border-slate-800 rounded-lg py-3 pl-12 pr-4 text-sm focus:outline-none focus:border-indigo-500 text-white placeholder-slate-500"
              placeholder="Search by Make, Model, City, or keyword..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <button className="flex items-center gap-2 px-6 py-3 bg-[#0D0D0E] border border-slate-800 rounded-lg hover:bg-slate-800 transition-colors text-sm font-medium text-slate-300">
            <Filter className="w-4 h-4" />
            Advanced Filters
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Filters Sidebar */}
        <aside className="w-72 border-r border-slate-800 bg-[#0D0D0E] overflow-y-auto p-6 hidden lg:block">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Filters</h3>
            <SlidersHorizontal className="w-4 h-4 text-slate-500" />
          </div>
          
          {/* Marketplace Filter */}
          <div className="mb-6">
            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Marketplace</h4>
            <div className="space-y-2">
              {['OLX', 'Facebook', 'Cars24', 'Spinny'].map(mp => (
                <label key={mp} className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" className="rounded border-slate-700 bg-slate-800 text-indigo-500 focus:ring-indigo-500 focus:ring-offset-slate-900" />
                  <span className="text-sm text-slate-300">{mp}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Price Range */}
          <div className="mb-6">
            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Price Range (₹)</h4>
            <div className="flex items-center gap-2">
              <input type="number" placeholder="Min" className="w-full bg-[#141416] border border-slate-700 rounded px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none" />
              <span className="text-slate-600">-</span>
              <input type="number" placeholder="Max" className="w-full bg-[#141416] border border-slate-700 rounded px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none" />
            </div>
          </div>

          {/* Year Range */}
          <div className="mb-6">
            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Registration Year</h4>
            <div className="flex items-center gap-2">
              <input type="number" placeholder="From" className="w-full bg-[#141416] border border-slate-700 rounded px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none" />
              <span className="text-slate-600">-</span>
              <input type="number" placeholder="To" className="w-full bg-[#141416] border border-slate-700 rounded px-3 py-1.5 text-sm focus:border-indigo-500 focus:outline-none" />
            </div>
          </div>

          {/* Fuel */}
          <div className="mb-6">
            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Fuel Type</h4>
            <div className="space-y-2">
              {['Petrol', 'Diesel', 'CNG', 'Electric'].map(f => (
                <label key={f} className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" className="rounded border-slate-700 bg-slate-800 text-indigo-500 focus:ring-indigo-500 focus:ring-offset-slate-900" />
                  <span className="text-sm text-slate-300">{f}</span>
                </label>
              ))}
            </div>
          </div>
        </aside>

        {/* Results */}
        <div className="flex-1 overflow-y-auto p-6 bg-[#0A0A0B]">
          <div className="flex justify-between items-center mb-6">
            <p className="text-sm text-slate-400">
              Showing <span className="font-bold text-white">{listings?.length || 0}</span> results
            </p>
            <div className="flex items-center gap-2 bg-[#141416] border border-slate-800 rounded-lg p-1">
              <button 
                onClick={() => setView('grid')} 
                className={`p-1.5 rounded ${view === 'grid' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <Grid className="w-4 h-4" />
              </button>
              <button 
                onClick={() => setView('list')} 
                className={`p-1.5 rounded ${view === 'list' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-[#141416] border border-slate-800 rounded-xl h-80 animate-pulse"></div>
              ))}
            </div>
          ) : (
            <div className={`grid gap-6 ${view === 'grid' ? 'grid-cols-1 md:grid-cols-2 xl:grid-cols-3' : 'grid-cols-1'}`}>
              {listings?.map((listing) => (
                <Link to={`/listing/${listing.id}`} key={listing.id} className="group bg-[#141416] border border-slate-800 rounded-xl overflow-hidden hover:border-indigo-500/50 transition-colors">
                  <div className={`${view === 'list' ? 'flex h-48' : 'block'}`}>
                    <div className={`relative bg-slate-900 overflow-hidden ${view === 'list' ? 'w-64 shrink-0' : 'h-48'}`}>
                      {listing.images && listing.images.length > 0 ? (
                        <img 
                          src={listing.images[0].image_url} 
                          alt={listing.title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-slate-700">No Image</div>
                      )}
                      {listing.deal_score && listing.deal_score > 8 && (
                        <div className="absolute top-3 left-3 bg-emerald-500 text-white text-[10px] font-bold px-2 py-1 rounded shadow">
                          GREAT DEAL
                        </div>
                      )}
                    </div>
                    <div className="p-5 flex-1 flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="text-white font-bold text-lg leading-tight line-clamp-2">{listing.title}</h3>
                          <div className="text-right shrink-0 ml-4">
                            <p className="text-emerald-400 font-bold text-lg">
                              ₹{listing.price.toLocaleString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 text-xs text-slate-400 mb-4">
                          <span className="bg-slate-800 px-2 py-1 rounded">{listing.registration_year}</span>
                          <span className="bg-slate-800 px-2 py-1 rounded">{listing.km_driven.toLocaleString()} km</span>
                          <span className="bg-slate-800 px-2 py-1 rounded">{listing.fuel}</span>
                          <span className="bg-slate-800 px-2 py-1 rounded">{listing.transmission}</span>
                        </div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-slate-500 border-t border-slate-800/50 pt-3">
                        <span className="truncate">{listing.registration_city}, {listing.registration_state}</span>
                        <span className="font-mono">{listing.marketplace?.name || 'Unknown'}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
              
              {(!listings || listings.length === 0) && (
                <div className="col-span-full flex flex-col items-center justify-center h-64 text-slate-500">
                  <Search className="w-12 h-12 mb-4 opacity-20" />
                  <p>No listings found matching your criteria.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
