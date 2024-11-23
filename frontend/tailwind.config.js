const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
        //display: ['Fredoka', ...defaultTheme.fontFamily.sans],
        display: ['Bangers', ...defaultTheme.fontFamily.sans]
      }
    }
  },
  plugins: [],
}
