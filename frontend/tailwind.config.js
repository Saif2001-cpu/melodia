/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Melodia brand palette
        primary: {
          50:  '#eef6ff',
          100: '#d9ebff',
          200: '#bbdcff',
          300: '#8dc5ff',
          400: '#59a4ff',
          500: '#3b82f6',  // primary accent
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        secondary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
          950: '#3b0764',
        },
        surface: {
          50:  '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#080d1a',  // deepest background
        },
        accent: {
          violet: '#8b5cf6',
          cyan:   '#06b6d4',
          emerald:'#10b981',
          rose:   '#f43f5e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'slide-up':      'slideUp 0.3s ease-out',
        'slide-down':    'slideDown 0.3s ease-out',
        'fade-in':       'fadeIn 0.2s ease-out',
        'spin-slow':     'spin 3s linear infinite',
        'pulse-slow':    'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'equalizer':     'equalizer 1.2s ease-in-out infinite',
      },
      keyframes: {
        slideUp: {
          '0%':   { transform: 'translateY(100%)', opacity: '0' },
          '100%': { transform: 'translateY(0)',    opacity: '1' },
        },
        slideDown: {
          '0%':   { transform: 'translateY(-100%)', opacity: '0' },
          '100%': { transform: 'translateY(0)',     opacity: '1' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        equalizer: {
          '0%, 100%': { transform: 'scaleY(0.4)' },
          '50%':      { transform: 'scaleY(1.0)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      screens: {
        xs: '480px',
      },
    },
  },
  plugins: [],
}
