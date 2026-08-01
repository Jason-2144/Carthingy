import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function AuthLayout() {
  const { user, isLoading } = useAuth();

  if (isLoading) return null;
  
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="min-h-screen bg-[#0A0A0B] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md flex flex-col items-center">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-5 h-5 bg-indigo-500 rounded-sm"></div>
          <span className="text-white font-bold tracking-tight text-3xl">
            CARSCOPE<span className="text-indigo-500">AI</span>
          </span>
        </div>
      </div>
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-[#141416] py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-slate-800">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
