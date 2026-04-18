import api from "./api";

export const interviewService = {
  generateQuestions: async (topic = "general") => {
    const res = await api.get(`/interview/generate?topic=${topic}`);
    return res.data;
  },
  evaluateAudio: async (sessionId, questionId, audioBlob) => {
    const form = new FormData();
    form.append("file", audioBlob, "answer.webm");
    const res = await api.post(
      `/interview/evaluate-audio/${sessionId}/${questionId}`,
      form
    );
    return res.data;
  },
  getSessionReport: async (sessionId) => {
    const res = await api.get(`/interview/session-report/${sessionId}`);
    return res.data;
  },
  getHistory: async () => {
    const res = await api.get("/interview/history");
    return res.data;
  },
  getStats: async () => {
    const res = await api.get("/interview/stats");
    return res.data;
  },
};
