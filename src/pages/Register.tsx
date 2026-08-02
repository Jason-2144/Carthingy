import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";
import { RegisterSchema, RegisterFormData } from "../types";
import { useState } from "react";
import { api } from "../services/api";

export default function Register() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(RegisterSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setError(null);
      await api.post("/auth/register", data);
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to register");
    }
  };

  return (
    <div>
      <h2 className="mt-2 mb-6 text-center text-2xl font-bold leading-9 tracking-tight text-white">
        Create an account
      </h2>

      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm p-3 rounded">
            {error}
          </div>
        )}

        <div>
          <label className="block text-sm font-medium leading-6 text-slate-300">
            Full Name
          </label>
          <div className="mt-2">
            <input
              {...register("full_name")}
              type="text"
              className="block w-full rounded-md border-0 bg-[#0D0D0E] py-1.5 text-white shadow-sm ring-1 ring-inset ring-slate-700 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
            />
            {errors.full_name && (
              <p className="mt-1 text-xs text-red-400">{errors.full_name.message}</p>
            )}
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium leading-6 text-slate-300">
            Email address
          </label>
          <div className="mt-2">
            <input
              {...register("email")}
              type="email"
              autoComplete="email"
              className="block w-full rounded-md border-0 bg-[#0D0D0E] py-1.5 text-white shadow-sm ring-1 ring-inset ring-slate-700 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
            />
            {errors.email && (
              <p className="mt-1 text-xs text-red-400">{errors.email.message}</p>
            )}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium leading-6 text-slate-300">
            Password
          </label>
          <div className="mt-2">
            <input
              {...register("password")}
              type="password"
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
            {isSubmitting ? "Creating..." : "Sign up"}
          </button>
        </div>
      </form>

      <p className="mt-10 text-center text-sm text-slate-400">
        Already have an account?{" "}
        <Link to="/login" className="font-semibold leading-6 text-indigo-400 hover:text-indigo-300">
          Sign in
        </Link>
      </p>
    </div>
  );
}
