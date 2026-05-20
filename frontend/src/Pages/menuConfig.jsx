// menuConfig.js - Palette de couleurs complète
export const COLORS = {
  // Couleurs principales - Thème moderne (bleu/gris)
  primary: {
    dark: "#1e293b",    // Slate 800
    main: "#3b82f6",    // Blue 500
    light: "#60a5fa",   // Blue 400
    lighter: "#dbeafe", // Blue 100
    bg: "#f8fafc",      // Slate 50
  },
  // Couleurs de survol et état actif
  active: {
    bg: "rgba(59, 130, 246, 0.15)",
    text: "#3b82f6",
    border: "#3b82f6",
  },
  // Neutres - Ajout de la propriété 'gray' complète
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
  },
  blanc: "#FFFFFF",
  noir: "#000000",
};

// La configuration des modules reste identique
export const modules = [
  {
    id: "dashboard",
    label: "TABLEAU DE BORD",
    icon: "📊",
    isDirect: true,
    key: "dashboard"
  },
  {
    id: "gestion",
    label: "GESTION",
    icon: "📋",
    submenus: [
      { key: "animaux", label: "Animaux", icon: "🐄", endpoint: "animaux" },
      { key: "enclos", label: "Enclos", icon: "🏡", endpoint: "enclos" },
      { key: "especes", label: "Espèces", icon: "🌿", endpoint: "especes" },
    ]
  },
  {
    id: "alimentation",
    label: "ALIMENTATION",
    icon: "🌾",
    submenus: [
      { key: "aliments", label: "Types d'aliments", icon: "📦", endpoint: "aliments" },
      { key: "stocks_aliments", label: "Stocks aliments", icon: "📊", endpoint: "stocks/aliments" },
      { key: "alimentations", label: "Alimentations", icon: "🍽️", endpoint: "alimentations" },
    ]
  },
  {
    id: "production_ventes",
    label: "PRODUCTION & VENTES",
    icon: "💰",
    submenus: [
      { key: "productions", label: "Productions", icon: "🥛", endpoint: "productions" },
      { key: "stocks_produits", label: "Stocks produits", icon: "📦", endpoint: "stocks/produits" },
      { key: "ventes", label: "Ventes", icon: "💵", endpoint: "ventes" },
    ]
  },
  {
    id: "sante_reproduction",
    label: "SANTÉ & REPRODUCTION",
    icon: "🏥",
    submenus: [
      { key: "sante", label: "Santé animale", icon: "🩺", endpoint: "sante" },
      { key: "reproduction", label: "Reproduction", icon: "🐣", endpoint: "reproductions" },
    ]
  },
  {
    id: "divers",
    label: "DIVERS",
    icon: "⚙️",
    submenus: [
      { key: "engrais", label: "Engrais", icon: "🌱", endpoint: "engrais" },
      { key: "utilisateurs", label: "Utilisateurs", icon: "👥", endpoint: "utilisateurs" },
    ]
  }
];