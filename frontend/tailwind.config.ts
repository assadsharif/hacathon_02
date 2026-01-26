import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: 'class',
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Productive Flow Theme
        primary: {
          DEFAULT: '#3b82f6',
          hover: '#2563eb',
        },
        success: {
          DEFAULT: '#10b981',
          hover: '#059669',
        },
        accent: {
          DEFAULT: '#8b5cf6',
          hover: '#7c3aed',
        },
        neutral: {
          DEFAULT: '#f3f4f6',
          border: '#e5e7eb',
        },
        danger: {
          DEFAULT: '#ef4444',
          hover: '#dc2626',
        },
        text: {
          primary: '#1f2937',
          secondary: '#6b7280',
        },
        background: "#f3f4f6",
        foreground: "#1f2937",
      },
      fontFamily: {
        sans: ['DejaVu Sans', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
