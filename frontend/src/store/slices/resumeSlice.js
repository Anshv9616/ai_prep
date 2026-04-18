import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { resumeService } from "../../services/resumeService";
import toast from "react-hot-toast";

export const uploadResumeThunk = createAsyncThunk(
  "resume/upload",
  async (file, { rejectWithValue }) => {
    const toastId = toast.loading("Uploading and indexing resume...");
    try {
      const res = await resumeService.upload(file);
      toast.success(`✓ ${res.total_chunks} chunks indexed`, { id: toastId });
      return res;
    } catch (err) {
      const msg = err.response?.data?.detail || "Upload failed";
      toast.error(msg, { id: toastId });
      return rejectWithValue(msg);
    }
  }
);

export const matchJDThunk = createAsyncThunk(
  "resume/matchJD",
  async (jobDescription, { rejectWithValue }) => {
    try {
      const res = await resumeService.matchJD(jobDescription);
      toast.success(`Match complete — ${res.match_score}% match`);
      return res;
    } catch (err) {
      const msg = err.response?.data?.detail || "Match failed";
      toast.error(msg);
      return rejectWithValue(msg);
    }
  }
);

export const coverLetterThunk = createAsyncThunk(
  "resume/coverLetter",
  async (jobDescription, { rejectWithValue }) => {
    try {
      const res = await resumeService.generateCoverLetter(jobDescription);
      toast.success("Cover letter generated!");
      return res;
    } catch (err) {
      const msg = err.response?.data?.detail || "Generation failed";
      toast.error(msg);
      return rejectWithValue(msg);
    }
  }
);

export const linkedinBioThunk = createAsyncThunk(
  "resume/linkedinBio",
  async (_, { rejectWithValue }) => {
    try {
      const res = await resumeService.getLinkedinBio();
      toast.success("LinkedIn bio generated!");
      return res;
    } catch (err) {
      const msg = err.response?.data?.detail || "Generation failed";
      toast.error(msg);
      return rejectWithValue(msg);
    }
  }
);

export const fetchResumeThunk = createAsyncThunk(
  "resume/fetch",
  async (_, { rejectWithValue }) => {
    try {
      return await resumeService.getMyResume();
    } catch (err) {
      return rejectWithValue("No resume found");
    }
  }
);

const resumeSlice = createSlice({
  name: "resume",
  initialState: {
    resume: null,
    uploadMsg: "",
    matchResult: null,
    coverLetter: null,
    linkedinBio: null,
    loading: false,
    matchLoading: false,
    coverLoading: false,
    linkedinLoading: false,
    error: null,
  },
  reducers: {
    clearResults: (state) => {
      state.matchResult = null;
      state.coverLetter = null;
      state.linkedinBio = null;
      state.error = null;
      state.uploadMsg = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadResumeThunk.pending, (state) => { state.loading = true; state.uploadMsg = ""; state.error = null; })
      .addCase(uploadResumeThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.uploadMsg = `✓ Uploaded — ${action.payload.total_chunks} chunks indexed`;
      })
      .addCase(uploadResumeThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(fetchResumeThunk.fulfilled, (state, action) => { state.resume = action.payload; })
      .addCase(matchJDThunk.pending, (state) => { state.matchLoading = true; state.matchResult = null; })
      .addCase(matchJDThunk.fulfilled, (state, action) => { state.matchLoading = false; state.matchResult = action.payload; })
      .addCase(matchJDThunk.rejected, (state, action) => { state.matchLoading = false; state.error = action.payload; })
      .addCase(coverLetterThunk.pending, (state) => { state.coverLoading = true; state.coverLetter = null; })
      .addCase(coverLetterThunk.fulfilled, (state, action) => { state.coverLoading = false; state.coverLetter = action.payload; })
      .addCase(coverLetterThunk.rejected, (state, action) => { state.coverLoading = false; state.error = action.payload; })
      .addCase(linkedinBioThunk.pending, (state) => { state.linkedinLoading = true; state.linkedinBio = null; })
      .addCase(linkedinBioThunk.fulfilled, (state, action) => { state.linkedinLoading = false; state.linkedinBio = action.payload; })
      .addCase(linkedinBioThunk.rejected, (state, action) => { state.linkedinLoading = false; state.error = action.payload; });
  },
});

export const { clearResults } = resumeSlice.actions;
export default resumeSlice.reducer;
