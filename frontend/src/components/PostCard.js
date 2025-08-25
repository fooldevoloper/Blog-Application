import Link from 'next/link';

const PostCard = ({ post }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-6 transition duration-300 hover:shadow-xl">
      <div className="p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          <Link href={`/posts/${post.id}`} className="hover:text-indigo-600 transition duration-300">
            {post.title}
          </Link>
        </h3>
        <div className="flex items-center text-gray-500 text-sm mb-4">
          <span className="font-medium text-indigo-600">{post.author}</span>
          <span className="mx-2">•</span>
          <span>{new Date(post.created_at).toLocaleDateString()}</span>
        </div>
        <p className="text-gray-700 leading-relaxed">
          {post.content.substring(0, 200)}...
        </p>
        <div className="mt-4">
          <Link href={`/posts/${post.id}`} className="text-indigo-600 hover:text-indigo-800 font-medium text-sm transition duration-300">
            Read more →
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PostCard;