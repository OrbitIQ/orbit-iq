import { useState, useEffect } from 'react';
import api from '@/services/AxiosInterceptor';
import RegistrationModal from './UserRegistrationModal';
import EditUserModal from './UserEditModal';

type User = {
    username: string;
    name: string;
    is_admin: boolean;
};

const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User>();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setIsEditModalOpen(true);
  };

  const handleUpdateUser = (updatedUser: User) => {
    setIsEditModalOpen(false);
    api.post(`/auth/edit`, {
      username: updatedUser.username,
      name: updatedUser.name,
      is_admin: updatedUser.is_admin
    }).then(() => {
      window.location.reload();
    })
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
  };

  useEffect(() => {
    api.get('/auth/list')
      .then(response => {
        // Assuming response.data.users is an array of User objects
        setUsers(response.data.users);
      })
      .catch(error => console.error(error));
  }, []);

  const handleCreateNewUser = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleDeleteUser = (username: string) => {
    if (!window.confirm(`Are you sure you want to delete the user "${username}"?`)) {
      return;
    }
    api.post(`/auth/delete`, {
      username: username
    }).then(() => {
      window.location.reload();
    })
  };

  return (
    <>
    {isEditModalOpen && editingUser && (
      <EditUserModal
        isOpen={isEditModalOpen}
        onClose={handleCloseEditModal}
        user={editingUser}
        onEdit={handleUpdateUser}
      />
    )}
    <div className="p-6 bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-semibold mb-4">User Management</h1>

      <div className="mb-4 text-left">
        <button 
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleCreateNewUser}
        >
          Create New User
        </button>
      </div>

      <RegistrationModal isOpen={isModalOpen} onClose={handleCloseModal} />

      {/* User list in a basic table */}
      <div className="mb-6">
        <table className="min-w-full leading-normal">
          <thead>
            <tr>
              <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Username
              </th>
              <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Full Name
              </th>
              <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Is Admin
              </th>
              <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100"></th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, index) => (
              <tr key={index}>
                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  {user.username}
                </td>
                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  {user.name}
                </td>
                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  {user.is_admin ? 'Yes' : 'No'}
                </td>
                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right">
                <button 
                    className="text-blue-600 hover:text-blue-900"
                    onClick={() => handleEditUser(user)}
                  >
                    Edit
                  </button>
                  <button 
                    className="text-red-600 hover:text-red-900 ml-4"
                    onClick={() => handleDeleteUser(user.username)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
    </>
  );
};

export default UserManagement;
