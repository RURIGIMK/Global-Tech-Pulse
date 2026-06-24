import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CalendarDays, ExternalLink, Share2, ArrowLeft } from 'lucide-react';

export default function ArticlePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/articles/${id}`)
      .then(res => res.json())
      .then(data => {
        setArticle(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  const shareArticle = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: article.title, url });
      } catch (err) {
        // user cancelled
      }
    } else {
      await navigator.clipboard.writeText(url);
      alert('Link copied to clipboard!');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  if (!article) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-10 text-center">
        <h2 className="text-2xl font-bold mb-4">Article not found</h2>
        <button onClick={() => navigate('/')} className="btn-primary inline-flex items-center gap-2">
          <ArrowLeft size={18} /> Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <button onClick={() => navigate('/')} className="mb-6 flex items-center gap-2 text-gray-500 hover:text-indigo-600 transition-colors">
        <ArrowLeft size={18} /> Back
      </button>
      <article className="glass-card p-6 sm:p-10">
        <img
          src={article.image}
          alt={article.title}
          className="w-full h-64 sm:h-96 object-cover rounded-xl mb-8"
        />
        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-4">
          <span className="flex items-center gap-1">
            <CalendarDays size={16} /> {new Date(article.publishedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
          </span>
          <span className="bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 px-3 py-1 rounded-full text-xs">
            {article.category}
          </span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold mb-6">{article.title}</h1>
        <div className="prose dark:prose-invert max-w-none mb-8">
          {article.summary.split('\n').map((p, i) => (
            <p key={i} className="mb-4 leading-relaxed">{p}</p>
          ))}
        </div>
        <div className="flex flex-wrap gap-4">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary inline-flex items-center gap-2"
          >
            <ExternalLink size={18} /> Read Original
          </a>
          <button
            onClick={shareArticle}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition"
          >
            <Share2 size={18} /> Share
          </button>
        </div>
      </article>
    </div>
  );
}