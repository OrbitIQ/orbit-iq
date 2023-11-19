import { useState } from 'react';
import Modal from 'react-modal';
import './EditModal.css';

Modal.setAppElement('#root'); // Set the app element

interface EditModalProps {
  onSave: (updateUser: string, updateNotes: string, updateData: any) => void;
  onCancel: () => void;
  isOpen: boolean;
  // Add updateUser and updateNotes to the interface
  updateUser?: string;
  updateNotes?: string;
    updateData: any;
}
const EditModal = ({
  onSave,
  onCancel,
  isOpen,
  updateUser: initialUpdateUser,
  updateNotes: initialUpdateNotes,
  updateData,
}: EditModalProps) => {
  const [updateUser, setUpdateUser] = useState(initialUpdateUser || '');
  const [updateNotes, setUpdateNotes] = useState(initialUpdateNotes || '');

  const handleSave = () => {
    onSave(updateUser, updateNotes, updateData);
  };

  return (
    <Modal isOpen={isOpen} onRequestClose={onCancel} contentLabel="Edit Modal">
      <div>
        <div>
          <label>User</label>
          <input
            type="text"
            value={updateUser}
            onChange={(e) => setUpdateUser(e.target.value)}
          />
        </div>
        <div>
          <label>Notes</label>
          <input
            type="text"
            value={updateNotes}
            onChange={(e) => setUpdateNotes(e.target.value)}
          />
        </div>
      </div>
      <div>
        <button onClick={handleSave}>Save</button>
        <button onClick={onCancel}>Cancel</button>
      </div>
    </Modal>
  );
};

export default EditModal;
