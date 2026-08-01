import { Archive, Search, MoreVertical } from "lucide-react";
import { Link } from "react-router-dom";

export default function SavedCars() {
  return (
    <div className="p-8 h-full flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Listing Archive</h1>
          <p className="text-sm text-slate-400 mt-1">Saved vehicles, favorites, and custom folders.</p>
        </div>
        <div className="flex gap-4">
          <div className="relative w-64">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-slate-500">
              <Search className="w-4 h-4" />
            </div>
            <input
              type="text"
              className="w-full bg-[#141416] border border-slate-700 rounded-md py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-indigo-500 text-white placeholder-slate-500"
              placeholder="Search saved..."
            />
          </div>
          <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded text-sm font-medium transition-colors">
            New Folder
          </button>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center border border-dashed border-slate-800 rounded-xl bg-[#0D0D0E]">
        <div className="text-center">
          <Archive className="w-12 h-12 text-slate-600 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-white mb-2">No saved listings yet</h3>
          <p className="text-sm text-slate-400 max-w-sm mx-auto mb-6">
            When you find interesting deals on the search page, save them here for later analysis and comparison.
          </p>
          <Link to="/search" className="bg-indigo-500 hover:bg-indigo-400 text-white px-6 py-2.5 rounded font-medium transition-colors">
            Go to Search
          </Link>
        </div>
      </div>
    </div>
  );
}
