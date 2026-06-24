import { Link } from 'react-router-dom';
import { CalendarDays, ExternalLink } from 'lucide-react';

export default function NewsCard({ article }) {
  return (
    <Link
      to={`/article/${article.id}`}
      className="group block animate-slide-up"
    >
      <article className="glass-card overflow-hidden h-full transform transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl">
        <div className="relative h-48 overflow-hidden">
          <img
            src={article.image}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = 'https://placehold.co/400x200?text=Tech+News';
            }}
          />
          <span className="absolute top-3 left-3 bg-indigo-600 text-white text-xs px-2 py-1 rounded-full">
            {article.category}
          </span>
        </div>
        <div className="p-4">
          <h3 className="font-semibold text-lg line-clamp-2 mb-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
            {article.title}
          </h3>
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 space-x-4 mt-3">
            <span className="flex items-center gap-1">
              <CalendarDays size={14} /> {new Date(article.publishedAt).toLocaleDateString()}
            </span>
            <span className="flex items-center gap-1">
              <ExternalLink size={14} /> {article.source}
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}