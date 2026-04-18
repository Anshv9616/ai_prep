import api from "./api";

export const resumeService = {
  upload: async (file) => {
    const form = new FormData();
    form.append("file", file);
    const res = await api.post("/resume/upload", form);
    return res.data;
  },
  getMyResume: async () => {
    const res = await api.get("/resume/my");
    return res.data;
  },
  matchJD: async (jobDescription) => {
    const form = new FormData();
    form.append("job_description", jobDescription);
    const res = await api.post("/resume/match-resume", form);
    return res.data;
  },
  generateCoverLetter: async (jobDescription) => {
    const form = new FormData();
    form.append("job_description", jobDescription);
    const res = await api.post("/resume/cover-letter", form);
    return res.data;
  },
  getLinkedinBio: async () => {
    const res = await api.get("/resume/linkedin-bio");
    return res.data;
  },
};
