import { useState, useRef } from "react";

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [duration, setDuration] = useState(0);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);
  const timer = useRef(null);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);
    chunks.current = [];
    mediaRecorder.current.ondataavailable = (e) => chunks.current.push(e.data);
    mediaRecorder.current.onstop = () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      setAudioBlob(blob);
      stream.getTracks().forEach((t) => t.stop());
    };
    mediaRecorder.current.start();
    setIsRecording(true);
    setDuration(0);
    timer.current = setInterval(() => setDuration((d) => d + 1), 1000);
  };

  const stop = () => {
    mediaRecorder.current?.stop();
    setIsRecording(false);
    clearInterval(timer.current);
  };

  const reset = () => { setAudioBlob(null); setDuration(0); };

  const fmt = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

  return { isRecording, audioBlob, duration, durationFmt: fmt(duration), start, stop, reset };
};
