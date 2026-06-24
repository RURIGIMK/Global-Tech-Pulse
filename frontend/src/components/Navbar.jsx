import ThemeToggle from './ThemeToggle';

export default function Navbar({ darkMode, toggleTheme }) {
  return (
    <header className="sticky top-0 z-50 mx-4 mt-4 glass-card p-4 flex justify-between items-center">
      <span className="text-xl font-bold bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent">
        Global Tech Pulse
      </span>
      <ThemeToggle darkMode={darkMode} toggle={toggleTheme} />
    </header>
  );
}