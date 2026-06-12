import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: "#0b1f3a",
        mission: "#17634f",
        sand: "#f7f1e5",
        signal: "#d64545"
      },
      boxShadow: { soft: "0 20px 60px rgba(11,31,58,0.12)" }
    }
  },
  plugins: []
};
export default config;
