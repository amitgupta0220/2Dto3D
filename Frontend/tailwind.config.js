/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Ensure this line is present
  ],
  theme: {
    extend: {
      colors: {
        blue: {
          500: "#007bff",
        },
        gray: {
          100: "#f7fafc",
          300: "#e2e8f0",
          600: "#718096",
        },
      },
    },
  },
  plugins: [],
};
