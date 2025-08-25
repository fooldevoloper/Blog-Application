import '../styles/globals.css';
import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import Head from 'next/head';
import { ToastProvider } from '../context/ToastContext';

function MyApp({ Component, pageProps }) {
  const { checkAuthStatus } = useAuthStore();

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  return (
    <ToastProvider>
      <Head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </Head>
      <Component {...pageProps} />
    </ToastProvider>
  );
}

export default MyApp;