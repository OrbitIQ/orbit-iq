import "./App.css";
import { useEffect } from 'react';
import Navbar from "./components/Navbar/Navbar";
import ChangelogPage from "./pages/ChangelogPage";
import DataPage from "./pages/DataPage";
import UpdatesPage from "./pages/UpdatesPage";
import { Routes, Route, Navigate } from "react-router-dom"; // Import Navigate
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';
import {queryClientContext} from './context';
import Logout from "./components/Authentication/Logout";
import Login from "./components/Authentication/Login";
import { ToastProvider, useToast } from "./components/Toast/ToastContext";
import { eventEmitter } from "./eventEmitter";
import MainLayout from "./Layouts/MainLayout";
import Register from "./components/Authentication/Register";
import ToastErrorWrapper from "./components/Toast/ToastErrorWrapper";
import UserManagement from "./components/Authentication/UserManagement";
import Account from "./components/Authentication/Account";

function App() {
  const queryClient = new QueryClient()

  return (
    <ToastProvider>
      <ToastErrorWrapper />
      <queryClientContext.Provider value = {{queryClient}}>
        <QueryClientProvider client={queryClient}>
          <Routes>
            <Route element={<MainLayout />}>
              <Route path="/" element={<DataPage />} />
              <Route path="/data" element={<DataPage />} />
              <Route path="/updates" element={<UpdatesPage />} />
              <Route path="/changelog" element={<ChangelogPage />} />
              <Route path="/users" element={<UserManagement />} /> {/* TODO: Restrict to just admins, need to store state if admin */}
              <Route path="/account" element={<Account /> } />
            </Route>
            <Route path="/logout" element={<Logout />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
          <ReactQueryDevtools/>
        </QueryClientProvider>
      </queryClientContext.Provider>
    </ToastProvider>
  );
}

export default App;