// tailwind.config.js
import plugin from "tailwindcss/plugin";

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  darkMode: "class",

  theme: {
    extend: {
      colors: {
        ui: {
          surface: "var(--ui-surface)",
          border: "var(--ui-border)",
          text: "var(--ui-text)",
          accent: "var(--ui-accent)",
          button: "var(--ui-button)",
          buttonHover: "var(--ui-button-hover)"
        },
      },

      boxShadow: {
        soft: "0 4px 14px rgba(15,23,42,0.10)",
        glass: "0 8px 28px rgba(15,23,42,0.12)",
        card: "0 6px 20px rgba(2,6,23,0.08)",
      },

      borderRadius: {
        xl: "14px",
        "2xl": "18px",
      },
    },
  },

  plugins: [
    require("@tailwindcss/forms"),
    plugin(function ({ addComponents, theme }) {

      addComponents({
        ".btn": {
          padding: ".45rem .9rem",
          borderRadius: theme("borderRadius.xl"),
          backgroundColor: "white",
          border: "1px solid var(--ui-border)",
          fontSize: ".85rem",
          boxShadow: theme("boxShadow.soft"),
        },

        ".btn-primary": {
          padding: ".45rem .9rem",
          borderRadius: theme("borderRadius.xl"),
          backgroundColor: "var(--ui-accent)",
          color: "white",
          boxShadow: "0 8px 20px rgba(99,102,241,0.35)",
        },

        ".btn-sm": {
          padding: ".3rem .65rem",
          borderRadius: theme("borderRadius.xl"),
          fontSize: ".8rem",
          backgroundColor: "white",
          border: "1px solid var(--ui-border)",
        },

        ".btn-outline": {
          padding: ".45rem .9rem",
          borderRadius: theme("borderRadius.xl"),
          backgroundColor: "transparent",
          border: "1px solid var(--ui-border)",
          color: "var(--ui-text)",
        },

        ".panel": {
          background: "var(--ui-surface)",
          borderRadius: theme("borderRadius.2xl"),
          border: "1px solid var(--ui-border)",
          boxShadow: theme("boxShadow.card"),
          padding: "1rem",
        }
      });
    }),
  ],
};
