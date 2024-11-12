// tailwind.config.js
module.exports = {
  content: [
    "./templates/**/*.html",  // Watch for HTML files in templates folder
  ],
  theme: {
    extend: {},  // You can extend the Tailwind theme if needed
  },
  plugins: [
    require('daisyui'),  // DaisyUI plugin
  ],
  daisyui: {
    themes: ["light", "dark", "cupcake", "lofi", "nord", "forest"],  // Available themes
  },
}
