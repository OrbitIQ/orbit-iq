import React, { useState } from 'react';

type User = {
    username: string;
    name: string;
    is_admin: boolean;
};

type EditUserModalProps = {
    isOpen: boolean;
    onClose: () => void;
    user: User;
    onEdit: (updatedUser: User) => void;
};

const EditUserModal: React.FC<EditUserModalProps> = ({ isOpen, onClose, user, onEdit }) => {
  const [username, setUsername] = useState(user.username);
  const [name, setName] = useState(user.name);
  const [isAdmin, setIsAdmin] = useState(user.is_admin);

  const handleEdit = (event: any) => {
    event.preventDefault();
    onEdit({ username, name, is_admin: isAdmin });
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <h3 className="text-lg font-semibold mb-4">Edit User</h3>
        <form onSubmit={handleEdit}>
          <input
            className="border p-2 w-full mb-3"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          <input
            className="border p-2 w-full mb-3"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Full Name"
          />
          <div className="flex items-center mb-4">
            <input
              type="checkbox"
              id="isAdmin"
              checked={isAdmin}
              onChange={(e) => setIsAdmin(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="isAdmin" className="text-sm font-medium">Is Admin</label>
          </div>
          <div className="flex justify-end">
            <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2">
              Update
            </button>
            <button onClick={onClose} className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditUserModal;
