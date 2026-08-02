import React, { createContext, useContext, useState, useEffect } from "react";
import { User, LoginFormData } from "../types";
import { api } from "../services/api";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (data: LoginFormData) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem("token");
      if (token) {
        const response = await api.get("/auth/me");
        setUser(response.data);
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
  }, []);

  const login = async (data: LoginFormData) => {
    const formData = new URLSearchParams();
    formData.append("username", data.username);
    formData.append("password", data.password);
    
    // FastAPI OAuth2PasswordRequestForm requires form-urlencoded
    const response = await api.post("/auth/login", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    
    localStorage.setItem("token", response.data.access_token);
    await checkAuth();
  };

  const logout = () => {
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
