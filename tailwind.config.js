/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
const plugin = require('tailwindcss/plugin');

module.exports = {
  content: [
    "./src/templates/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    colors: {
      primary: {
        "50": "#eff6ff",
        "100": "#243b6d",
        "200": "#bfdbfe",
        "300": "#93c5fd",
        "400": "#60a5fa",
        "500": "#3b82f6",
        "600": "#2563eb",
        "700": "#1d4ed8",
        "800": "#1e40af",
        "900": "#1e3a8a",
        "950": "#172554"
      },
      white: colors.white,
      black: colors.black,
      cv: {
        "100": "1c2a30",
      },
      cvBlue: {
        "100": "#a8c4c8",
        "900": "#6391a0",
      },
      stone: colors.stone,
      sky: colors.sky,
      violet: colors.violet,
      gray: colors.gray,
      blue: colors.blue,
      red: colors.red,
      green: colors.green,
      neutral: colors.neutral
    },
    fontFamily: {
      'body': [
        'Inter',
        'ui-sans-serif',
        'system-ui',
        '-apple-system',
        'system-ui',
        'Segoe UI',
        'Roboto',
        'Helvetica Neue',
        'Arial',
        'Noto Sans',
        'sans-serif',
        'Apple Color Emoji',
        'Segoe UI Emoji',
        'Segoe UI Symbol',
        'Noto Color Emoji'
      ],
      'sans': [
        'Inter',
        'ui-sans-serif',
        'system-ui',
        '-apple-system',
        'system-ui',
        'Segoe UI',
        'Roboto',
        'Helvetica Neue',
        'Arial',
        'Noto Sans',
        'sans-serif',
        'Apple Color Emoji',
        'Segoe UI Emoji',
        'Segoe UI Symbol',
        'Noto Color Emoji'
      ]
    },
    extend: {},
  },

  plugins: [
    require('flowbite/plugin'),
    plugin(function ({ addVariant }) {
      addVariant('htmx', ({ modifySelectors, separator }) => {
        modifySelectors(({ className }) => {
          return `.htmx-request .htmx\\:${className}`;
        });
      });
    }),
  ],
}