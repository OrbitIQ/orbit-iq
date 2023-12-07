import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '@/services/AxiosInterceptor'; // Adjust the import path as needed

const UserSettings: React.FC = () => {
  const navigate = useNavigate();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleLogout = () => {
    navigate('/logout');
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!oldPassword || !newPassword) {
      setError('Both old and new passwords are required.');
      return;
    }

    try {
      const response = await api.post('/auth/changepassword', {
        old_password: oldPassword,
        new_password: newPassword,
      });

      setError('');
      setSuccess(response.data.msg);
      setOldPassword('');
      setNewPassword('');
    } catch (error: any) {
      setError(error.response.data.msg || 'An error occurred.');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl mb-4">User Settings</h1>
      {error && <p className="text-red-500">{error}</p>}
      {success && <p className="text-green-500">{success}</p>}
      <form onSubmit={handleChangePassword} className="mb-4">
        <div className="mb-2">
          <label htmlFor="old-password" className="block mb-1 font-bold">
            Current Password
          </label>
          <input
            id="old-password"
            type="password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            className="border-2 rounded-md p-2 w-full"
          />
        </div>
        <div className="mb-2">
          <label htmlFor="new-password" className="block mb-1 font-bold">
            New Password
          </label>
          <input
            id="new-password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            className="border-2 rounded-md p-2 w-full"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-md">
          Change Password
        </button>
      </form>
      <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded-md">
        Logout
      </button>
    </div>
  );
};

export default UserSettings;
