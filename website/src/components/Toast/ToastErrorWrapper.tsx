import React, { useEffect } from 'react';
import { useToast } from './ToastContext'; // Adjust the path as needed
import { eventEmitter } from '../../eventEmitter'; // Adjust the path as needed

const ToastErrorWrapper: React.FC = () => {
  const { showToast } = useToast();

  useEffect(() => {
    const handleApiError = (msg: string) => {
      showToast(msg);
    };

    eventEmitter.on('apiError', handleApiError); // Listen for apiError events
    eventEmitter.on('error', handleApiError); // Listen for error events (for non-API errors)

    return () => {
      eventEmitter.off('apiError', handleApiError); // Clean up the listener
      eventEmitter.off('error', handleApiError); // Clean up the listener
    };
  }, [showToast]);

  // This component doesn't render anything itself
  return null;
};

export default ToastErrorWrapper;
