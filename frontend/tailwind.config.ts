import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#0b1020',
        panel: '#111827',
        panel2: '#0f172a',
        line: '#243046',
        text: '#e5eefb',
        muted: '#8aa0c7',
        accent: '#60a5fa',
      },
    },
  },
  plugins: [],
} satisfies Config
