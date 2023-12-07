// ToastContext.tsx
import React, { Fragment, createContext, useContext, useState } from "react";

interface ToastContextType {
  showToast: (message: string) => void;
}

const ToastContext = createContext<ToastContextType>({
  showToast: () => {
    
  },
});

export const useToast = () => useContext(ToastContext);

const TOAST_DURATION = 10000; // Duration of the toast in milliseconds (e.g., 10000ms for 10 seconds)
const UPDATE_INTERVAL = 10; // Update interval for the progress bar in milliseconds (e.g., 10ms)

type ToastProviderProps = {
  children: React.ReactNode;
};

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  const [message, setMessage] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(100);

  const showToast = (msg: string) => {
    setMessage(msg);
    setProgress(100);

    const totalSteps = TOAST_DURATION / UPDATE_INTERVAL;
    const decrementAmount = 100 / totalSteps;

    const interval = setInterval(() => {
      setProgress(prevProgress => Math.max(prevProgress - decrementAmount, 0));
    }, UPDATE_INTERVAL);

    setTimeout(() => {
      setMessage(null);
      clearInterval(interval);
    }, TOAST_DURATION);
  };

  const dismissToast = () => {
    setMessage(null);
  };

  const renderMessage = (message: string) => {
    return message.split('\n').map((item, key) => (
      <Fragment key={key}>
        {item}
        <br />
      </Fragment>
    ));
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {message && (
        <div className="fixed bottom-5 right-5 bg-red-500 text-white py-2 px-4 rounded flex items-center justify-between">
          <span>{renderMessage(message)}</span>
          <button onClick={dismissToast} className="text-white ml-4">
            &#10005;
          </button>
          <div
            className="absolute bottom-0 left-0 right-0 bg-red-700 h-1"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}
    </ToastContext.Provider>
  );
};
