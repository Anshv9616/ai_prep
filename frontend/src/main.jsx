import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "./store/store";
import App from "./App";
import "./index.css";
import {Toaster} from "react-hot-toast"
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 3000,
          style: {
            background: "#0d0e1a",
            color: "#f0eeff",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: "12px",
            fontSize: "13.5px",
            fontFamily: "'Plus Jakarta Sans', sans-serif",
          },
          success: {
            iconTheme: { primary: "#4ade80", secondary: "#0d0e1a" },
          },
          error: {
            iconTheme: { primary: "#f87171", secondary: "#0d0e1a" },
          },
        }}
      />
    </Provider>
  </React.StrictMode>
);
