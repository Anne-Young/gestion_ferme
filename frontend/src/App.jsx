import { BrowserRouter, Routes, Route } from 'react-router-dom';
import FermeGestLandings from "./Pages/FermeGestLandings";
import DashboardLayout from "./Pages/DashboardLayout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FermeGestLandings />} />
        <Route path="/dashboard/*" element={<DashboardLayout />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;