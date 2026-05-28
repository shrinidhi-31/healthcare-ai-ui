import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#0F172A] text-white">
      <nav className="flex items-center justify-between px-10 py-6">
        <h1 className="text-3xl font-bold">MediAssist</h1>

        <Link to="/dashboard">
          <button className="rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 px-6 py-3 shadow-lg transition-all duration-300 hover:scale-105">
            Open Dashboard
          </button>
        </Link>
      </nav>

      <section className="flex flex-col items-center justify-between gap-10 px-10 py-20 md:flex-row">
        <div className="max-w-xl">
          <p className="mb-4 tracking-widest text-cyan-400">
            AI Powered Healthcare Routing
          </p>

          <h1 className="mb-6 text-6xl font-bold leading-tight">
            Smarter <br />
            Healthcare System
          </h1>

          <p className="mb-8 text-lg leading-relaxed text-gray-300">
            MediAssist uses artificial intelligence to analyze symptoms,
            prioritize emergencies, route patients to nearby specialists, and
            assist healthcare professionals in real time.
          </p>

          <div className="flex gap-4">
            <Link to="/dashboard">
              <button className="rounded-2xl bg-gradient-to-r from-blue-500 to-cyan-400 px-6 py-3 shadow-xl transition-all duration-300 hover:scale-105">
                Launch Dashboard
              </button>
            </Link>

            <button className="rounded-2xl border border-gray-500 px-6 py-3 transition-all duration-300 hover:bg-white hover:text-black">
              Learn More
            </button>
          </div>
        </div>

        <div className="w-full max-w-md rounded-3xl border border-white/20 bg-white/10 p-8 shadow-2xl backdrop-blur-lg">
          <h2 className="mb-6 text-2xl font-semibold">Live AI Routing</h2>

          <div className="space-y-4">
            <div className="rounded-2xl bg-[#1E293B] p-4">
              Heart: Chest Pain → Cardiology
            </div>
            <div className="rounded-2xl bg-[#1E293B] p-4">
              Fever: Fever → General Medicine
            </div>
            <div className="rounded-2xl bg-[#1E293B] p-4">
              Bone: Fracture → Orthopedics
            </div>
            <div className="rounded-2xl bg-[#1E293B] p-4">
              Report: AI Report Analysis Completed
            </div>
          </div>
        </div>
      </section>

      <section className="px-10 pb-20">
        <h2 className="mb-14 text-center text-4xl font-bold">Core Features</h2>

        <div className="grid gap-8 md:grid-cols-3">
          <div className="rounded-3xl border border-white/10 bg-white/10 p-8 backdrop-blur-lg transition-all duration-300 hover:-translate-y-2">
            <h3 className="mb-4 text-2xl font-semibold">Smart Routing</h3>
            <p className="text-gray-300">
              AI analyzes patient symptoms and routes them to the most suitable
              healthcare specialist instantly.
            </p>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/10 p-8 backdrop-blur-lg transition-all duration-300 hover:-translate-y-2">
            <h3 className="mb-4 text-2xl font-semibold">
              Emergency Detection
            </h3>
            <p className="text-gray-300">
              Detects high-priority medical emergencies and triggers urgent
              notifications immediately.
            </p>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/10 p-8 backdrop-blur-lg transition-all duration-300 hover:-translate-y-2">
            <h3 className="mb-4 text-2xl font-semibold">AI Assistance</h3>
            <p className="text-gray-300">
              Assists doctors with patient history, report summaries, and
              treatment recommendations.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
