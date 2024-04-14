module.exports = {
  content: [
    './products/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    colors: {
      primary: '#FF6347',
      secondary: '#F2F0F1',
      accent: '#4CAF50',
      white: '#FFFFFF',
      black: '#000000',
    },
    spacing: {
      '1': '0.25rem',
      '2': '0.5rem',
      '3': '0.75rem',
      '4': '1rem',
      '5': '1.25rem',
    },
    fontFamily: {
      sans: ['Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },

    extend: {
      screens: {
        '2xl': '1440px',
      },
      boxShadow: {
        'custom': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
      opacity: {
        '90': '0.9',
        '95': '0.95',
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],

}