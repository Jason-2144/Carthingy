import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router-dom";
import { useState } from "react";
import { api } from "../services/api";

const ForgotPasswordSchema = z.object({
  email: z.string().email(),
});

type ForgotPasswordData = z.infer<typeof ForgotPasswordSchema>;

export default function ForgotPassword() {
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ForgotPasswordData>({
    resolver: zodResolver(ForgotPasswordSchema)
  });

  const onSubmit = async (data: ForgotPasswordData) => {
    try {
      setError(null);
      await api.post("/auth/forgot-password", data); // assuming backend has this
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Something went wrong.");
    }
  };

  if (success) {
    return (
      <div className="text-center">
        <h2 className="mt-2 text-2xl font-bold leading-9 tracking-tight text-white mb-4">Check your email</h2>
        <p className="text-slate-400 mb-8">We've sent password reset instructions to your email address.</p>
        <Link to="/login" className="text-indigo-400 hover:text-indigo-300 font-medium">Return to Login</Link>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mt-2 mb-2 text-center text-2xl font-bold leading-9 tracking-tight text-white">
        Reset your password
      </h2>
      <p className="text-center text-sm text-slate-400 mb-8">Enter your email address and we'll send you a link to reset your password.</p>

      <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm p-3 rounded">
            {error}
          </div>
        )}
        
        <div>
          <label className="block text-sm font-medium leading-6 text-slate-300">Email address</label>
          <div className="mt-2">
            <input
              {...register("email")}
              type="email"
              className="block w-full rounded-md border-0 bg-[#0D0D0E] py-1.5 text-white shadow-sm ring-1 ring-inset ring-slate-700 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
            />
            {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email.message}</p>}
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 disabled:opacity-50"
          >
            {isSubmitting ? "Sending..." : "Send Reset Link"}
          </button>
        </div>
      </form>

      <p className="mt-10 text-center text-sm text-slate-400">
        Remember your password?{" "}
        <Link to="/login" className="font-semibold leading-6 text-indigo-400 hover:text-indigo-300">
          Sign in
        </Link>
      </p>
    </div>
  );
}
