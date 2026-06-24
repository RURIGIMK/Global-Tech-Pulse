import Navbar from './Navbar';

export default function Layout({ children, darkMode, toggleTheme }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar darkMode={darkMode} toggleTheme={toggleTheme} />
      <main className="flex-1">{children}</main>
      <footer className="text-center text-sm text-gray-400 dark:text-gray-600 py-4">
        © {new Date().getFullYear()} Global Tech Pulse · Fresh news every hour
      </footer>
    </div>
  );
}