import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { registerThunk, clearError } from "../store/slices/authSlice";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [done, setDone] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((s) => s.auth);

  useEffect(() => () => dispatch(clearError()), []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await dispatch(registerThunk({ email, password }));
    if (!res.error) { setDone(true); setTimeout(() => navigate("/login"), 1500); }
  };

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center p-6 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-accent top-0 left-0 -translate-x-1/2 -translate-y-1/2" />
      <div className="orb w-72 h-72 bg-violet-600 bottom-0 right-0 translate-x-1/2 translate-y-1/2" />
      <div className="absolute inset-0 opacity-[0.03]"
        style={{ backgroundImage: "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)", backgroundSize: "48px 48px" }} />

      <div className="w-full max-w-sm relative z-10 animate-fade-up">
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent to-accent-light flex items-center justify-center text-white font-black text-lg shadow-glow mb-4 animate-float">
            AI
          </div>
          <h1 className="text-2xl font-bold text-white">Create account</h1>
          <p className="text-white/40 text-sm mt-1">Start your interview journey</p>
        </div>

        <div className="glass-strong rounded-2xl p-6 gradient-border">
          {error && <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm animate-fade-in">{error}</div>}
          {done && <div className="mb-4 p-3 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-sm animate-fade-in">Account created! Redirecting...</div>}
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-white/40 uppercase tracking-wider">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com" required
                className="bg-bg-4/60 border border-border-2 rounded-xl px-4 py-2.5 text-sm text-white placeholder-white/20 focus:outline-none focus:border-accent/60 focus:bg-bg-5/60 transition-all duration-200" />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-white/40 uppercase tracking-wider">Password</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="Min 6 characters" required minLength={6}
                className="bg-bg-4/60 border border-border-2 rounded-xl px-4 py-2.5 text-sm text-white placeholder-white/20 focus:outline-none focus:border-accent/60 focus:bg-bg-5/60 transition-all duration-200" />
            </div>
            <button type="submit" disabled={loading || done}
              className="btn-shine mt-1 w-full py-3 rounded-xl bg-accent text-white font-semibold text-sm hover:bg-accent/90 transition-all duration-200 shadow-glow-sm disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2">
              {loading ? <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Creating...</> : "Create Account →"}
            </button>
          </form>
          <p className="text-center text-xs text-white/25 mt-5">
            Have an account? <Link to="/login" className="text-accent-light hover:text-accent transition-colors">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
