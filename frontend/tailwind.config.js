/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        bg: {
          DEFAULT: "#07080f",
          2: "#0d0e1a",
          3: "#121420",
          4: "#181a28",
          5: "#1e2035",
        },
        accent: {
          DEFAULT: "#7c5cfc",
          light: "#a78bfa",
          glow: "rgba(124,92,252,0.25)",
        },
        border: {
          DEFAULT: "rgba(255,255,255,0.07)",
          2: "rgba(255,255,255,0.11)",
          3: "rgba(255,255,255,0.18)",
        },
      },
      animation: {
        "fade-up": "fadeUp 0.4s ease forwards",
        "fade-in": "fadeIn 0.3s ease forwards",
        "slide-in": "slideIn 0.35s ease forwards",
        "pulse-slow": "pulse 3s ease-in-out infinite",
        "wave": "wave 0.7s ease-in-out infinite alternate",
        "glow": "glow 2s ease-in-out infinite alternate",
        "spin-slow": "spin 3s linear infinite",
        "float": "float 3s ease-in-out infinite",
        "shimmer": "shimmer 2s linear infinite",
      },
      keyframes: {
        fadeUp: { "0%": { opacity: 0, transform: "translateY(16px)" }, "100%": { opacity: 1, transform: "translateY(0)" } },
        fadeIn: { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        slideIn: { "0%": { opacity: 0, transform: "translateX(-12px)" }, "100%": { opacity: 1, transform: "translateX(0)" } },
        wave: { "0%": { height: "4px" }, "100%": { height: "28px" } },
        glow: { "0%": { boxShadow: "0 0 20px rgba(124,92,252,0.2)" }, "100%": { boxShadow: "0 0 40px rgba(124,92,252,0.5)" } },
        float: { "0%,100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-6px)" } },
        shimmer: { "0%": { backgroundPosition: "-200% 0" }, "100%": { backgroundPosition: "200% 0" } },
      },
      backdropBlur: { xs: "2px" },
      boxShadow: {
        glow: "0 0 30px rgba(124,92,252,0.3)",
        "glow-sm": "0 0 15px rgba(124,92,252,0.2)",
        card: "0 4px 24px rgba(0,0,0,0.4)",
      },
    },
  },
  plugins: [],
};
