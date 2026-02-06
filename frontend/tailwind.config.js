/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Space Grotesk", "Pretendard", "Noto Sans KR", "sans-serif"],
      },
      colors: {
        ink: "#0f172a",
        mist: "#e2e8f0",
        neon: "#0ea5e9",
        coral: "#fb7185",
        lime: "#84cc16",
      },
      boxShadow: {
        float: "0 20px 40px -20px rgba(15, 23, 42, 0.5)",
      },
      keyframes: {
        rise: {
          "0%": { opacity: 0, transform: "translateY(10px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: {
        rise: "rise 550ms ease forwards",
      },
    },
  },
  plugins: [],
};
