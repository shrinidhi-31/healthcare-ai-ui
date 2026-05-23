import Layout from "../components/Layout"

export default function Notifications() {

  return (

    <Layout>

      <div className="space-y-6">

        {/* Header */}

        <div className="flex justify-between items-center">

          <div>

            <h1 className="text-4xl font-bold text-[#0F172A]">
              Notifications
            </h1>

            <p className="text-gray-500 mt-2">
              Real-time healthcare alerts and updates.
            </p>

          </div>

        </div>

        {/* Notification Cards */}

        <div className="space-y-4">

          <div className="bg-red-50 rounded-3xl p-6 shadow-lg border border-red-200">

            <h2 className="text-red-600 text-xl font-bold">
              Emergency Alert
            </h2>

            <p className="text-gray-700 mt-2">
              Critical patient routing detected near Downtown Medical Center.
            </p>

          </div>

          <div className="bg-blue-50 rounded-3xl p-6 shadow-lg border border-blue-200">

            <h2 className="text-blue-600 text-xl font-bold">
              Report Uploaded
            </h2>

            <p className="text-gray-700 mt-2">
              New healthcare report successfully analyzed by AI system.
            </p>

          </div>

          <div className="bg-green-50 rounded-3xl p-6 shadow-lg border border-green-200">

            <h2 className="text-green-600 text-xl font-bold">
              Doctor Available
            </h2>

            <p className="text-gray-700 mt-2">
              Specialist doctor is now available for emergency consultation.
            </p>

          </div>

        </div>

      </div>

    </Layout>

  )
}