import Link from 'next/link';
import { useAuthStore } from '../store/authStore';
import { useRouter } from 'next/router';

const Header = () => {
  const { user, isAuthenticated, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center text-white font-bold text-2xl">
              <span className="bg-white text-indigo-600 rounded-lg px-2 py-1 mr-2">B</span>
              BlogSpace
            </Link>
            <nav className="ml-10 flex space-x-8">
              <Link href="/" className="text-indigo-100 hover:text-white inline-flex items-center px-1 pt-1 text-sm font-medium transition duration-300">
                Home
              </Link>
            </nav>
          </div>
          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <span className="text-white font-medium">Hello, {user?.username}</span>
                <button
                  onClick={handleLogout}
                  className="bg-white text-indigo-600 hover:bg-indigo-50 px-4 py-2 rounded-md text-sm font-medium transition duration-300 shadow-md"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex space-x-4">
                <Link href="/login" className="text-indigo-100 hover:text-white px-4 py-2 rounded-md text-sm font-medium transition duration-300">
                  Login
                </Link>
                <Link href="/register" className="bg-white text-indigo-600 hover:bg-indigo-50 px-4 py-2 rounded-md text-sm font-medium transition duration-300 shadow-md">
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;