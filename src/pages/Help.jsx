import Layout from "../components/Layout"

export default function Help() {

  return (

    <Layout>

      <div className="space-y-6">

        {/* Header */}

        <div>

          <h1 className="text-4xl font-bold text-[#0F172A]">
            Help & Support
          </h1>

          <p className="text-gray-500 mt-2">
            Learn more about the healthcare AI system.
          </p>

        </div>

        {/* FAQ Cards */}

        <div className="space-y-4">

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-xl font-bold text-[#0F172A]">
              How does AI routing work?
            </h2>

            <p className="text-gray-500 mt-2">
              The AI analyzes symptoms and routes patients to nearby specialists.
            </p>

          </div>

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-xl font-bold text-[#0F172A]">
              How are emergency cases handled?
            </h2>

            <p className="text-gray-500 mt-2">
              Critical symptoms trigger ambulance and emergency hospital suggestions.
            </p>

          </div>

          <div className="bg-white/80 backdrop-blur-lg rounded-3xl p-6 shadow-lg border border-white/40">

            <h2 className="text-xl font-bold text-[#0F172A]">
              Can AI analyze reports?
            </h2>

            <p className="text-gray-500 mt-2">
              Yes, uploaded healthcare reports are processed for insights and urgency detection.
            </p>

          </div>

        </div>

      </div>

    </Layout>

  )
}