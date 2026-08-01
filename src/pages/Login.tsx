import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { LoginSchema, LoginFormData } from "../types";
import { useState } from "react";

export default function Login() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(LoginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      setError(null);
      await login(data);
    } catch (err: any) {
      setError(err.message || "Failed to login");
    }
  };

  return (
    <div>
      <h2 className="mt-2 mb-6 text-center text-2xl font-bold leading-9 tracking-tight text-white">
        Sign in to your account
      </h2>

      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm p-3 rounded">
            {error}
          </div>
        )}
        
        <div>
          <label className="block text-sm font-medium leading-6 text-slate-300">
            Email address
          </label>
          <div className="mt-2">
            <input
              {...register("username")}
              type="email"
              autoComplete="email"
              className="block w-full rounded-md border-0 bg-[#0D0D0E] py-1.5 text-white shadow-sm ring-1 ring-inset ring-slate-700 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
            />
            {errors.username && (
              <p className="mt-1 text-xs text-red-400">{errors.username.message}</p>
            )}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between">
            <label className="block text-sm font-medium leading-6 text-slate-300">
              Password
            </label>
            <div className="text-sm">
              <a href="#" className="font-semibold text-indigo-400 hover:text-indigo-300">
                Forgot password?
              </a>
            </div>
          </div>
          <div className="mt-2">
            <input
              {...register("password")}
              type="password"
              autoComplete="current-password"
              className="block w-full rounded-md border-0 bg-[#0D0D0E] py-1.5 text-white shadow-sm ring-1 ring-inset ring-slate-700 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
            />
            {errors.password && (
              <p className="mt-1 text-xs text-red-400">{errors.password.message}</p>
            )}
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:opacity-50"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </div>
      </form>

      <p className="mt-10 text-center text-sm text-slate-400">
        Not a member?{" "}
        <Link to="/register" className="font-semibold leading-6 text-indigo-400 hover:text-indigo-300">
          Create an account
        </Link>
      </p>
    </div>
  );
}
