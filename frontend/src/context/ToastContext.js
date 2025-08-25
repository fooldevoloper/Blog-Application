import { createContext, useContext, useState } from 'react';
import Toast from '../components/Toast';

const ToastContext = createContext();

let toastId = 0;
const generateId = () => ++toastId;

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = (message, type = 'info', duration = 3000) => {
    const id = generateId();
    const newToast = { id, message, type, duration };
    setToasts((prevToasts) => [...prevToasts, newToast]);

    // Auto remove toast after duration
    const timer = setTimeout(() => {
      removeToast(id);
    }, duration);

    // Store timer reference to clear if needed
    newToast.timer = timer;
  };

  const removeToast = (id) => {
    setToasts((prevToasts) => {
      const toastToRemove = prevToasts.find(toast => toast.id === id);
      if (toastToRemove && toastToRemove.timer) {
        clearTimeout(toastToRemove.timer);
      }
      return prevToasts.filter(toast => toast.id !== id);
    });
  };

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}
      <div className="toast-container fixed top-4 right-4 z-50 space-y-2">
        {toasts.map((toast, index) => (
          <div
            key={toast.id}
            className="transform transition-all duration-300 ease-in-out"
            style={{
              transition: 'all 0.3s ease-in-out',
              transform: `translateY(${index * 10}px) scale(${1 - index * 0.05})`
            }}
          >
            <Toast
              message={toast.message}
              type={toast.type}
              duration={toast.duration}
              onClose={() => removeToast(toast.id)}
            />
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};