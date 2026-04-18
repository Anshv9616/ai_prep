import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { authService } from "../../services/authService";
import toast from "react-hot-toast";
export const loginThunk = createAsyncThunk(
  "auth/login",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const data = await authService.login(email, password);
      localStorage.setItem("token", data.access_token);
      toast.success("Welcome back!");
      return data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || "Login failed";
toast.error(errorMessage);
return rejectWithValue(errorMessage);
     
    }
  }
);

export const registerThunk = createAsyncThunk(
  "auth/register",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const data = await authService.register(email, password);
      toast.success("Account created!");
      return data;
    } catch (err) {
      const msg = err.response?.data?.detail || "Registration failed";
      toast.error(msg);
      return rejectWithValue(msg);
    }
  }
);
const authSlice = createSlice({
  name: "auth",
  initialState: {
    token: localStorage.getItem("token") || null,
    isAuthenticated: !!localStorage.getItem("token"),
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      localStorage.removeItem("token");
      state.token = null;
      state.isAuthenticated = false;
      state.error = null;
    },
    clearError: (state) => { state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload.access_token;
        state.isAuthenticated = true;
      })
      .addCase(loginThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(registerThunk.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(registerThunk.fulfilled, (state) => { state.loading = false; })
      .addCase(registerThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
