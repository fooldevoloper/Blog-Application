import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { api } from '../../../lib/api';
import { useAuthStore } from '../../../store/authStore';
import Header from '../../../components/Header';
import PostForm from '../../../components/PostForm';
import { useToast } from '../../../context/ToastContext';

export default function EditPost() {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const { id } = router.query;
  const { isAuthenticated, user } = useAuthStore();
  const { showToast } = useToast();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    } else if (id) {
      fetchPost();
    }
  }, [isAuthenticated, id, router]);

  const fetchPost = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/posts/${id}/`);
      const postData = response.data.post;
      
      // Check if user is the author
      if (postData.author !== user?.username) {
        router.push('/');
        return;
      }
      
      setPost(postData);
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch post';
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

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

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {post && <PostForm post={post} />}
      </div>
    </div>
  );
}