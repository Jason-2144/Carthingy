import { useAuth } from "../contexts/AuthContext";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="p-8 h-full overflow-y-auto">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-white tracking-tight mb-8">User Settings</h1>
        
        <div className="bg-[#141416] border border-slate-800 rounded-lg overflow-hidden mb-8">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-lg font-bold text-white">Profile Information</h2>
            <p className="text-sm text-slate-400 mt-1">Update your account details and preferences.</p>
          </div>
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Full Name</label>
                <input 
                  type="text" 
                  defaultValue={user?.full_name}
                  className="w-full bg-[#0D0D0E] border border-slate-700 rounded-md py-2 px-3 text-white focus:outline-none focus:border-indigo-500" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
                <input 
                  type="email" 
                  defaultValue={user?.email}
                  disabled
                  className="w-full bg-[#0D0D0E] border border-slate-800 rounded-md py-2 px-3 text-slate-500 cursor-not-allowed" 
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Role</label>
              <div className="inline-block bg-slate-800 text-slate-300 px-3 py-1 rounded text-sm font-medium">
                {user?.is_superuser ? 'Administrator' : 'Analyst'}
              </div>
            </div>
            
            <div className="pt-4 flex justify-end">
              <button className="bg-indigo-500 hover:bg-indigo-400 text-white px-6 py-2 rounded text-sm font-medium transition-colors">
                Save Changes
              </button>
            </div>
          </div>
        </div>

        <div className="bg-[#141416] border border-slate-800 rounded-lg overflow-hidden">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-lg font-bold text-white">API Keys</h2>
            <p className="text-sm text-slate-400 mt-1">Manage API keys for programmatic access to the data engine.</p>
          </div>
          <div className="p-6">
            <div className="border border-dashed border-slate-700 rounded-lg p-8 text-center">
              <p className="text-slate-400 text-sm mb-4">You don't have any active API keys.</p>
              <button className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded text-sm font-medium transition-colors">
                Generate New Key
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
