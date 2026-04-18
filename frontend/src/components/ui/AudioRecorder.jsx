import { useAudioRecorder } from "../../hooks/useAudioRecorder";

export default function AudioRecorder({ onSubmit, loading }) {
  const { isRecording, audioBlob, durationFmt, start, stop, reset } = useAudioRecorder();

  return (
    <div className="glass rounded-2xl p-6 flex flex-col items-center gap-5 animate-fade-up">
      
      <div className={`flex items-center gap-[3px] h-10 ${isRecording ? "recording" : ""}`}>
        {Array.from({ length: 28 }).map((_, i) => (
          <span
            key={i}
            className="waveform-bar"
            style={{ animationDelay: `${i * 0.035}s` }}
          />
        ))}
      </div>

      {/* Timer */}
      <div className="font-mono text-3xl font-bold text-white/50 tracking-widest">
        {durationFmt}
      </div>

      {/* Controls */}
      <div className="flex flex-col items-center gap-4 w-full">
        {!isRecording && !audioBlob && (
          <button
            onClick={start}
            className="btn-shine flex items-center gap-2 px-8 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 font-semibold text-sm hover:bg-red-500/20 transition-all duration-200 hover:border-red-500/40"
          >
            <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse" />
            Start Recording
          </button>
        )}
        {isRecording && (
          <button
            onClick={stop}
            className="flex items-center gap-2 px-8 py-3 rounded-xl bg-red-500/20 border border-red-500/40 text-red-400 font-semibold text-sm hover:bg-red-500/30 transition-all duration-200 animate-pulse-slow"
          >
            <span className="w-3 h-3 rounded-sm bg-red-400" />
            Stop Recording
          </button>
        )}
        {audioBlob && !isRecording && (
          <div className="w-full flex flex-col gap-3">
            <audio controls src={URL.createObjectURL(audioBlob)} className="w-full rounded-xl accent-accent" />
            <div className="flex gap-3">
              <button
                onClick={reset}
                className="flex-1 py-2.5 rounded-xl bg-white/5 border border-border-2 text-white/50 text-sm font-medium hover:bg-white/8 hover:text-white/80 transition-all"
              >
                ↺ Re-record
              </button>
              <button
                onClick={() => onSubmit(audioBlob)}
                disabled={loading}
                className="btn-shine flex-1 py-2.5 rounded-xl bg-accent text-white text-sm font-semibold hover:bg-accent/90 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-glow-sm"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Evaluating...
                  </span>
                ) : "Submit Answer →"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
