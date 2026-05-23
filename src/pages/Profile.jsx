import Layout from "../components/Layout"

export default function Profile() {

  return (

    <Layout>

      <div className="space-y-6">

        {/* Profile Header */}

        <div
          className="
          bg-white/80
          backdrop-blur-lg
          rounded-3xl
          p-8
          shadow-lg
          border border-white/40
          flex items-center justify-between
        "
        >

          <div>

            <h1 className="text-4xl font-bold text-[#0F172A]">
              Dr. Sharma
            </h1>

            <p className="text-gray-500 mt-2">
              Senior Cardiologist
            </p>

          </div>

          <div className="w-24 h-24 rounded-full bg-gradient-to-r from-blue-500 to-cyan-400"></div>

        </div>

        {/* Stats */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-gray-500">
              Patients
            </h2>

            <p className="text-4xl font-bold mt-4">
              124
            </p>

          </div>

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-gray-500">
              Experience
            </h2>

            <p className="text-4xl font-bold mt-4">
              15 yrs
            </p>

          </div>

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-gray-500">
              Cases Solved
            </h2>

            <p className="text-4xl font-bold mt-4">
              98%
            </p>

          </div>

        </div>

      </div>

    </Layout>

  )
}