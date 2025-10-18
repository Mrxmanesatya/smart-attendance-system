import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "../utils/axios";
import { API_ENDPOINTS } from "../config/api";
import toast from "react-hot-toast";

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("token"));

  // Load user on mount if token exists
  useEffect(() => {
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.ME);
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      const response = await axios.post(API_ENDPOINTS.REGISTER, userData);
      toast.success("Registration successful! Please login.");
      return { success: true, data: response.data };
    } catch (error) {
      const message = error.response?.data?.detail || "Registration failed";
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const login = async (credentials) => {
    try {
      const response = await axios.post(API_ENDPOINTS.LOGIN, credentials);
      const { access_token } = response.data;

      localStorage.setItem("token", access_token);
      setToken(access_token);

      // Fetch user details
      const userResponse = await axios.get(API_ENDPOINTS.ME);
      setUser(userResponse.data);

      toast.success("Login successful!");
      return { success: true, user: userResponse.data };
    } catch (error) {
      const message = error.response?.data?.detail || "Login failed";
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
    toast.success("Logged out successfully");
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    register,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
