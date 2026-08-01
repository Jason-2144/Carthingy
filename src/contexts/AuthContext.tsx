import React, { createContext, useContext, useState, useEffect } from "react";
import { User, LoginFormData } from "../types";
import { supabase } from "../services/supabase";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: LoginFormData) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.user) {
        // Map Supabase user to our User type
        setUser({
          id: session.user.id,
          email: session.user.email || '',
          full_name: session.user.user_metadata?.full_name || '',
          is_active: true,
          is_superuser: false,
          created_at: session.user.created_at
        });
        localStorage.setItem("token", session.access_token);
      } else {
        setUser(null);
        localStorage.removeItem("token");
      }
    } catch (error) {
      setUser(null);
      localStorage.removeItem("token");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
    
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (session?.user) {
        setUser({
          id: session.user.id,
          email: session.user.email || '',
          full_name: session.user.user_metadata?.full_name || '',
          is_active: true,
          is_superuser: false,
          created_at: session.user.created_at
        });
        localStorage.setItem("token", session.access_token);
      } else {
        setUser(null);
        localStorage.removeItem("token");
      }
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const login = async (data: LoginFormData) => {
    const { data: authData, error } = await supabase.auth.signInWithPassword({
      email: data.username,
      password: data.password,
    });
    
    if (error) {
      throw error;
    }
    
    if (authData.session) {
      localStorage.setItem("token", authData.session.access_token);
    }
  };

  const logout = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
