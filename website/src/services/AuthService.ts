// AuthService.ts
import { AxiosResponse } from "axios";
import { useState, useEffect } from 'react';
import api from "./AxiosInterceptor";


interface LoginResponse {
  access_token: string;
}

const register = async (username: string, name: string, password: string): Promise<AxiosResponse> => {
  return api.post(`/auth/register`, {
    username,
    name,
    password,
  });
};

const login = async (username: string, password: string): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>(`/auth/login`, {
    username,
    password,
  });

  if (response.data.access_token) {
    localStorage.setItem('user', JSON.stringify(response.data));
    await checkAdminStatus();
  }

  return response.data;
};

const logout = (): void => {
  localStorage.removeItem('user');
  localStorage.removeItem('isAdmin');
};

const deleteUser = async (username: string): Promise<AxiosResponse> => {
  const user = JSON.parse(localStorage.getItem('user') || '{}') as LoginResponse;
  if (user && user.access_token) {
    return api.post(
      `/auth/delete`, 
      { username },
      { headers: { 'Authorization': `Bearer ${user.access_token}` } }
    );
  }
  throw new Error('User is not logged in.');
};

const checkAdminStatus = async (): Promise<boolean> => {
  try {
    const response = await api.get('/auth/isadmin');
    const isAdmin = response.data.admin;
    localStorage.setItem('isAdmin', JSON.stringify(isAdmin));
    return isAdmin;
  } catch (error) {
    console.error("Error checking admin status:", error);
    return false;
  }
};

const isAuth = (): boolean => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  return Boolean(user.access_token);
};

export default {
  register,
  login,
  logout,
  deleteUser,
  checkAdminStatus,
  isAuth
};
