/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: '#2563eb',
        accent: '#14b8a6',
      },
    },
  },
  plugins: [],
}
