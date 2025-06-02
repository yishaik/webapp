import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MainPage from './pages/MainPage'; // Import MainPage
import HistoryView from './pages/HistoryView'; // Import HistoryView
import HistoryDetailPage from './pages/HistoryDetailPage'; // Import HistoryDetailPage

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white flex flex-col">
        {/* Header */}
        <header className="bg-gray-800 shadow-md">
          <nav className="container mx-auto px-6 py-3">
            <div className="flex items-center justify-between">
              <Link to="/" className="text-xl font-semibold text-white hover:text-indigo-300 transition-colors">
                PromptForge
              </Link>
              <div>
                <Link to="/" className="px-3 py-2 text-gray-300 hover:text-indigo-300 transition-colors">
                  Forge
                </Link>
                <Link to="/history" className="px-3 py-2 text-gray-300 hover:text-indigo-300 transition-colors">
                  History
                </Link>
              </div>
            </div>
          </nav>
        </header>

        {/* Main Content */}
        <main className="flex-grow container mx-auto px-6 py-8">
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/history" element={<HistoryView />} />
            <Route path="/history/:promptId" element={<HistoryDetailPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-gray-800 shadow-md mt-auto">
          <div className="container mx-auto px-6 py-4 text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} PromptForge. All rights reserved.
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;