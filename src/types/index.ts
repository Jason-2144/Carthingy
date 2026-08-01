import { z } from "zod";

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Listing {
  id: string;
  marketplace_id: string;
  seller_id: string;
  external_listing_id: string;
  url: string;
  title: string;
  description: string;
  price: number;
  market_value?: number;
  deal_score?: number;
  price_difference?: number;
  registration_year: number;
  km_driven: number;
  ownership: number;
  fuel: string;
  transmission: string;
  colour: string;
  registration_state: string;
  registration_city: string;
  first_seen: string;
  last_seen: string;
  is_active: boolean;
  marketplace?: { id: string; name: string };
  seller?: { id: string; name: string; contact_info?: string };
  images: { id: string; image_url: string; order: number }[];
  history?: { id: string; old_price: number; new_price: number; timestamp: string }[];
}

export const LoginSchema = z.object({
  username: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(1, { message: "Password is required" }),
});
export type LoginFormData = z.infer<typeof LoginSchema>;

export const RegisterSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  full_name: z.string().min(2),
});
export type RegisterFormData = z.infer<typeof RegisterSchema>;
