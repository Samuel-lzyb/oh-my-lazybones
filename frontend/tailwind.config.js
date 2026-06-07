/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts,js}'],
  theme: {
    extend: {
      colors: {
        'bg-deep': '#0D0D1A',
        'bg-card': '#1A1A30',
        'bg-hover': '#252545',
        'brand-amber': '#F59E0B',
        'brand-deep': '#D97706',
        'text-soft': '#E8E8F0',
        'text-dim': '#9CA3AF',
        'accent-green': '#34D399',
        'border-subtle': '#2D2D45',
      },
      fontFamily: {
        display: ['Outfit', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        card: '12px',
        btn: '8px',
        input: '6px',
      },
    },
  },
  plugins: [],
}
