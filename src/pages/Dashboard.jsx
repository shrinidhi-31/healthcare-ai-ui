import Layout from "../components/Layout"
import {
  Activity,
  ShieldAlert,
  FileText,
  Users
} from "lucide-react"

export default function Dashboard() {

  return (

    <Layout>

      <div className="space-y-6">

        {/* Top Header */}

        <div className="flex justify-between items-center mb-8">

          <div>

            <h1 className="text-4xl font-bold text-[#0F172A]">
              Dashboard
            </h1>

            <p className="text-gray-500 mt-2">
              Welcome back to the healthcare AI system.
            </p>

          </div>

          <button className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white px-6 py-3 rounded-2xl shadow-lg hover:scale-105 transition-all duration-300">

            Emergency Action

          </button>

        </div>

        {/* Stats Cards */}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-6
            shadow-lg
            border border-white/40
            hover:-translate-y-1
            transition-all duration-300
          "
          >

            <div className="flex items-center justify-between">

  <h2 className="text-gray-500">
    Total Patients
  </h2>

  <Users size={28} className="text-blue-500" />

</div>

            <p className="text-4xl font-bold mt-4 text-[#0F172A]">
              1,284
            </p>

            <p className="text-green-500 mt-2 font-medium">
              +12% this week
            </p>

          </div>

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-6
            shadow-lg
            border border-white/40
            hover:-translate-y-1
            transition-all duration-300
          "
          >

            <div className="flex items-center justify-between">

  <h2 className="text-gray-500">
    Emergency Cases
  </h2>

  <ShieldAlert size={28} className="text-red-500" />

</div>

            <p className="text-4xl font-bold mt-4 text-red-500">
              32
            </p>

            <p className="text-red-400 mt-2 font-medium">
              High priority alerts
            </p>

          </div>

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-6
            shadow-lg
            border border-white/40
            hover:-translate-y-1
            transition-all duration-300
          "
          >

            <div className="flex items-center justify-between">

  <h2 className="text-gray-500">
    Doctors Available
  </h2>

  <Activity size={28} className="text-green-500" />

</div>

            <p className="text-4xl font-bold mt-4 text-blue-600">
              24
            </p>

            <p className="text-blue-400 mt-2 font-medium">
              Active specialists
            </p>

          </div>

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-6
            shadow-lg
            border border-white/40
            hover:-translate-y-1
            transition-all duration-300
          "
          >

            <div className="flex items-center justify-between">

  <h2 className="text-gray-500">
    Reports Uploaded
  </h2>

  <FileText size={28} className="text-cyan-500" />

</div>

            <p className="text-4xl font-bold mt-4 text-[#0F172A]">
              563
            </p>

            <p className="text-green-500 mt-2 font-medium">
              AI analyzed reports
            </p>

          </div>

        </div>

        {/* Emergency Section */}

        <div
          className="
          bg-red-50
          rounded-3xl
          p-8
          shadow-lg
          border border-red-200
        "
        >

          <h2 className="text-2xl font-bold text-red-600">
            Emergency Alert
          </h2>

          <p className="text-gray-700 mt-3">
            Critical patient routing detected near Downtown Medical Center.
          </p>

          <div className="mt-6 flex gap-4">

            <button className="bg-red-500 text-white px-6 py-3 rounded-2xl hover:bg-red-600 transition-all duration-300">

              Call Ambulance

            </button>

            <button className="bg-white border border-red-300 text-red-500 px-6 py-3 rounded-2xl hover:bg-red-100 transition-all duration-300">

              View Details

            </button>

          </div>

        </div>

        {/* Bottom Grid */}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* AI Routing */}

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-8
            shadow-lg
            border border-white/40
          "
          >

            <h2 className="text-2xl font-bold text-[#0F172A]">
              AI Smart Routing
            </h2>

            <p className="text-gray-500 mt-3">
              AI automatically detects urgency levels and routes patients to the nearest healthcare specialist.
            </p>

            <div className="mt-6 space-y-4">

              <div className="bg-blue-50 p-4 rounded-2xl border border-blue-100">
                Chest Pain → Cardiology Department
              </div>

              <div className="bg-green-50 p-4 rounded-2xl border border-green-100">
                Fever → General Medicine
              </div>

              <div className="bg-yellow-50 p-4 rounded-2xl border border-yellow-100">
                Bone Fracture → Orthopedics
              </div>

            </div>

          </div>

          {/* Recent Activity */}

          <div
            className="
            bg-white/80
            backdrop-blur-lg
            rounded-3xl
            p-8
            shadow-lg
            border border-white/40
          "
          >

            <h2 className="text-2xl font-bold text-[#0F172A]">
              Recent Activity
            </h2>

            <div className="mt-6 space-y-5">

              <div className="flex justify-between items-center border-b pb-4">

                <div>

                  <p className="font-semibold">
                    AI Report Analysis Completed
                  </p>

                  <p className="text-gray-500 text-sm">
                    2 mins ago
                  </p>

                </div>

                <span className="bg-green-100 text-green-600 px-4 py-2 rounded-xl text-sm">
                  Success
                </span>

              </div>

              <div className="flex justify-between items-center border-b pb-4">

                <div>

                  <p className="font-semibold">
                    Emergency Ambulance Triggered
                  </p>

                  <p className="text-gray-500 text-sm">
                    15 mins ago
                  </p>

                </div>

                <span className="bg-red-100 text-red-600 px-4 py-2 rounded-xl text-sm">
                  Critical
                </span>

              </div>

              <div className="flex justify-between items-center">

                <div>

                  <p className="font-semibold">
                    New Patient Registered
                  </p>

                  <p className="text-gray-500 text-sm">
                    30 mins ago
                  </p>

                </div>

                <span className="bg-blue-100 text-blue-600 px-4 py-2 rounded-xl text-sm">
                  New
                </span>

              </div>

            </div>

          </div>

        </div>

      </div>

    </Layout>

  )
}