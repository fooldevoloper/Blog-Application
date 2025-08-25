import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { api } from '../../lib/api';
import Header from '../../components/Header';
import Link from 'next/link';
import { useAuthStore } from '../../store/authStore';
import { useToast } from '../../context/ToastContext';

export default function PostDetail() {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const { id } = router.query;
  const { user, isAuthenticated } = useAuthStore();
  const { showToast } = useToast();

  useEffect(() => {
    if (id) {
      fetchPost();
    }
  }, [id]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/posts/${id}/`);
      setPost(response.data.post);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch post');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      try {
        await api.delete(`/posts/${id}/`);
        showToast('Post deleted successfully!', 'success');
        router.push('/');
      } catch (err) {
        const errorMessage = err.response?.data?.error || 'Failed to delete post';
        showToast(errorMessage, 'error');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
        <Header />
        <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <p>Loading post...</p>
          </div>
        </div>
      </div>
    );
  }

  const isAuthor = isAuthenticated && post && user && post.author === user.username;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {post && (
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">{post.title}</h1>
                  <div className="flex items-center text-gray-500 text-sm">
                    <span className="font-medium text-indigo-600">{post.author}</span>
                    <span className="mx-2">•</span>
                    <span>{new Date(post.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}</span>
                  </div>
                </div>
                {isAuthor && (
                  <div className="flex space-x-2">
                    <Link href={`/posts/${post.id}/edit`} className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300">
                      Edit
                    </Link>
                    <button
                      onClick={handleDelete}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-300"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
              <div className="prose max-w-none text-gray-700 whitespace-pre-line leading-relaxed">
                {post.content}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}