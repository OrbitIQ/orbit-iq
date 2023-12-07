import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Perform logout operations
    localStorage.removeItem('user'); // Remove user data from local storage

    // Redirect to login page
    navigate('/login');
  }, [history]);

  return (
    <div>
      Logging out...
    </div>
  );
};

export default Logout;
