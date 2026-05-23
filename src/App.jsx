import { Routes, Route } from "react-router-dom"

import LandingPage from "./pages/LandingPage"
import Dashboard from "./pages/Dashboard"
import Reports from "./pages/Reports"
import Settings from "./pages/Settings"
import Profile from "./pages/Profile"
import Notifications from "./pages/Notifications"
import Help from "./pages/Help"

export default function App() {
  return (
    <Routes>

      <Route path="/" element={<LandingPage />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/reports" element={<Reports />} />

      <Route path="/settings" element={<Settings />} />

      <Route path="/profile" element={<Profile />} />

      <Route path="/notifications" element={<Notifications />} />

      <Route path="/settings" element={<Settings />} />

      <Route path="/help" element={<Help />} />

    </Routes>
  )
}