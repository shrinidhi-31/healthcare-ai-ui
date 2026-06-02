import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Smartphone,
  ShieldCheck,
  ArrowLeft,
} from "lucide-react";

export default function DoctorSignIn() {
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");

  const sendOtp = () => {
    if (!phone) {
      alert("Enter phone number");
      return;
    }

    setOtpSent(true);

    alert("OTP Sent Successfully");
  };

  const verifyOtp = () => {
    if (otp === "123456") {
      localStorage.setItem("role", "doctor");

      navigate("/dashboard");
    } else {
      alert("Invalid OTP");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#071133] to-[#0F172A] flex items-center justify-center px-6">

      <div className="w-full max-w-xl">

        {/* Back */}

        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-slate-400 hover:text-white mb-8"
        >
          <ArrowLeft size={18} />
          Back
        </button>

        {/* Card */}

        <div className="bg-white/10 backdrop-blur-xl rounded-[32px] p-10 border border-white/10 shadow-2xl">

          <div className="flex justify-center mb-8">

            <div className="w-20 h-20 rounded-3xl bg-cyan-500/20 flex items-center justify-center">

              <ShieldCheck
                size={42}
                className="text-cyan-400"
              />

            </div>

          </div>

          <h1 className="text-4xl font-bold text-center text-white">
            Doctor Sign In
          </h1>

          <p className="text-slate-400 text-center mt-3">
            Secure OTP Authentication
          </p>

          {/* Phone */}

          <div className="mt-10">

            <label className="text-slate-300 text-sm">
              Phone Number
            </label>

            <div className="mt-3 flex items-center gap-3 bg-white/10 rounded-2xl px-5 py-4 border border-white/10">

              <Smartphone
                className="text-cyan-400"
                size={20}
              />

              <input
                type="tel"
                placeholder="Enter Registered Phone Number"
                value={phone}
                onChange={(e) =>
                  setPhone(e.target.value)
                }
                className="bg-transparent outline-none flex-1 text-white"
              />

            </div>

          </div>

          {/* Send OTP */}

          {!otpSent && (

            <button
              onClick={sendOtp}
              className="
                w-full
                mt-8
                bg-gradient-to-r
                from-blue-500
                to-cyan-400
                py-4
                rounded-2xl
                font-semibold
                shadow-xl
                hover:scale-105
                transition-all
              "
            >
              Send OTP
            </button>

          )}

          {/* OTP */}

          {otpSent && (

            <>
              <div className="mt-8">

                <label className="text-slate-300 text-sm">
                  Enter OTP
                </label>

                <input
                  type="text"
                  placeholder="123456"
                  value={otp}
                  onChange={(e) =>
                    setOtp(e.target.value)
                  }
                  className="
                    mt-3
                    w-full
                    bg-white/10
                    border
                    border-white/10
                    rounded-2xl
                    px-5
                    py-4
                    text-white
                    outline-none
                  "
                />

              </div>

              <button
                onClick={verifyOtp}
                className="
                  w-full
                  mt-8
                  bg-gradient-to-r
                  from-blue-500
                  to-cyan-400
                  py-4
                  rounded-2xl
                  font-semibold
                  shadow-xl
                  hover:scale-105
                  transition-all
                "
              >
                Verify OTP
              </button>

            </>
          )}

        </div>

      </div>

    </div>
  );
}