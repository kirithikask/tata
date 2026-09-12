import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Overview from './pages/Overview';
import Diagnose from './pages/Diagnose';
import Memory from './pages/Memory';
import Machines from './pages/Machines';
import Evidence from './pages/Evidence';
import Cases from './pages/Cases';
import Benchmark from './pages/Benchmark';
import FailureAnalysis from './pages/FailureAnalysis';
import './App.css';

const navItems = [
  { to: '/', label: 'Overview' },
  { to: '/diagnose', label: 'Diagnose' },
  { to: '/memory', label: 'Memory' },
  { to: '/machines', label: 'Machines' },
  { to: '/evidence', label: 'Evidence' },
  { to: '/cases', label: 'Cases' },
  { to: '/benchmark', label: 'Benchmark' },
  { to: '/failure-analysis', label: 'Failure Analysis' },
];

function App() {
  return (
    <BrowserRouter>
      <header className="app-header">
        <div className="app-title">ENGINEERING MEMORY</div>
        <nav className="app-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
              end={item.to === '/'}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="app-status">● System Online</div>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/diagnose" element={<Diagnose />} />
          <Route path="/memory" element={<Memory />} />
          <Route path="/machines" element={<Machines />} />
          <Route path="/evidence" element={<Evidence />} />
          <Route path="/cases" element={<Cases />} />
          <Route path="/benchmark" element={<Benchmark />} />
          <Route path="/failure-analysis" element={<FailureAnalysis />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;