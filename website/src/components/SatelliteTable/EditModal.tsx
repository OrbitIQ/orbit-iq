import { useState } from 'react';
import Modal from 'react-modal';

// Set the app element
Modal.setAppElement('#root');

interface EditModalProps {
  onSave: (updateNotes: string, updateData: any) => void;
  onCancel: () => void;
  isOpen: boolean;
  updateNotes?: string;
  updateData: any;
}

const EditModal = ({
  onSave,
  onCancel,
  isOpen,
  updateNotes: initialUpdateNotes,
  updateData,
}: EditModalProps) => {
  const [updateNotes, setUpdateNotes] = useState(initialUpdateNotes || '');

  const handleSave = () => {
    onSave(updateNotes, updateData);
  };

  return (
    <Modal isOpen={isOpen} onRequestClose={onCancel} contentLabel="Edit Modal" style={modalStyle}>
      <div>
        <div style={inputContainerStyle}>
          <label style={labelStyle}>Notes</label>
          <textarea
            value={updateNotes}
            onChange={(e) => setUpdateNotes(e.target.value)}
            style={{ ...inputStyle, height: '80px', resize: 'none' }}
          />
        </div>
      </div>
      <div style={buttonContainerStyle}>
        <button onClick={handleSave} style={saveButtonStyle}>
          Save
        </button>
        <button onClick={onCancel} style={cancelButtonStyle}>
          Cancel
        </button>
      </div>
    </Modal>
  );
};

// Define inline styles
const modalStyle: ReactModal.Styles = {
    overlay: {
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
    },
    content: {
      backgroundColor: '#fff',
      padding: '50px',
      borderRadius: '8px',
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.2)',
      maxWidth: '600px',
      width: '100%',
      maxHeight: '80vh',
      margin: 'auto', // Center horizontally
      overflow: 'auto',
    },
};

const inputContainerStyle: React.CSSProperties = {
  marginBottom: '15px',
};

const labelStyle: React.CSSProperties = {
  display: 'block',
  marginBottom: '5px',
  fontWeight: 'bold',
};

const inputStyle: React.CSSProperties = {
  width: 'calc(100% - 16px)',
  padding: '8px',
  border: '1px solid #ccc',
  borderRadius: '4px',
  boxSizing: 'border-box',
  marginTop: '3px',
};

const buttonContainerStyle: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  marginTop: '15px',
};

const buttonStyle: React.CSSProperties = {
  padding: '10px',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
  margin: '0 5px',
};

const saveButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: '#4caf50',
  color: 'white',
};

const cancelButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: '#f44336',
  color: 'white',
};

export default EditModal;
