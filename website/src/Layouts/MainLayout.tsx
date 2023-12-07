import React from 'react';
import Navbar from '../components/Navbar/Navbar';
import { Outlet } from 'react-router-dom'; // Import Outlet

const MainLayout: React.FC = () => {
  return (
    <>
      <Navbar />
      <div>
        <Outlet /> {/* This is where nested routes will be rendered */}
      </div>
    </>
  );
};

export default MainLayout;
