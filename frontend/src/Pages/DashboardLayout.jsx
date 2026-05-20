// DashboardLayout.jsx - Version corrigée sans warnings
import { useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import Sidebar from "./Sidebar";
import { COLORS } from "./menuConfig";

// Composants des différents modules
import Dashboard from "./modules/Dashboard";
import Animaux from "./modules/Animaux";
import Enclos from "./modules/Enclos";
import Especes from "./modules/Especes";
import Aliments from "./modules/Aliments";
import StocksAliments from "./modules/StocksAliments";
import Alimentations from "./modules/Alimentations";
import Productions from "./modules/Productions";
import StocksProduits from "./modules/StocksProduits";
import Ventes from "./modules/Ventes";
import Sante from "./modules/Sante";
import Reproduction from "./modules/Reproduction";
import Engrais from "./modules/Engrais";
import Utilisateurs from "./modules/Utilisateurs";

// Fonction pour déterminer l'état actif à partir du chemin
function getActiveStateFromPath(pathname) {
  const pathParts = pathname.split('/').filter(part => part !== 'dashboard' && part !== '');
  
  if (pathParts.length === 0) {
    return { active: "dashboard", activeModule: null };
  } else if (pathParts.length === 1) {
    const submenuKey = pathParts[0];
    
    // Trouver quel module parent contient ce sous-menu
    const modulesList = [
      { id: "gestion", submenus: ["animaux", "enclos", "especes"] },
      { id: "alimentation", submenus: ["aliments", "stocks_aliments", "alimentations"] },
      { id: "production_ventes", submenus: ["productions", "stocks_produits", "ventes"] },
      { id: "sante_reproduction", submenus: ["sante", "reproduction"] },
      { id: "divers", submenus: ["engrais", "utilisateurs"] }
    ];
    
    const parent = modulesList.find(m => m.submenus.includes(submenuKey));
    return { active: submenuKey, activeModule: parent ? parent.id : null };
  } else if (pathParts.length >= 2) {
    return { active: pathParts[1], activeModule: pathParts[0] };
  }
  
  return { active: "dashboard", activeModule: null };
}

function DashboardLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [localActiveModule, setLocalActiveModule] = useState(null); // Pour l'état local du sidebar
  
  // Calculer l'état actif directement pendant le rendu (pas dans useEffect)
  const { active, activeModule } = getActiveStateFromPath(location.pathname);

  const getTitle = () => {
    const titles = {
      dashboard: "Tableau de bord",
      animaux: "Gestion des Animaux",
      enclos: "Gestion des Enclos",
      especes: "Gestion des Espèces",
      aliments: "Types d'aliments",
      stocks_aliments: "Stocks aliments",
      alimentations: "Alimentations",
      productions: "Productions",
      stocks_produits: "Stocks produits",
      ventes: "Ventes",
      sante: "Santé animale",
      reproduction: "Reproduction",
      engrais: "Engrais",
      utilisateurs: "Utilisateurs",
    };
    return titles[active] || "FermeGest";
  };

  const renderContent = () => {
    switch(active) {
      case "dashboard":
        return <Dashboard />;
      case "animaux":
        return <Animaux />;
      case "enclos":
        return <Enclos />;
      case "especes":
        return <Especes />;
      case "aliments":
        return <Aliments />;
      case "stocks_aliments":
        return <StocksAliments />;
      case "alimentations":
        return <Alimentations />;
      case "productions":
        return <Productions />;
      case "stocks_produits":
        return <StocksProduits />;
      case "ventes":
        return <Ventes />;
      case "sante":
        return <Sante />;
      case "reproduction":
        return <Reproduction />;
      case "engrais":
        return <Engrais />;
      case "utilisateurs":
        return <Utilisateurs />;
      default:
        return <Dashboard />;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate('/');
  };

  // Fonction pour mettre à jour la route quand on clique sur un menu
  const handleSetActive = (newActive, newActiveModule) => {
    if (newActive === "dashboard") {
      navigate('/dashboard');
    } else if (newActiveModule) {
      navigate(`/dashboard/${newActiveModule}/${newActive}`);
    } else {
      navigate(`/dashboard/${newActive}`);
    }
  };

  // Mettre à jour l'état local du module actif pour le sidebar
  const handleSetActiveModule = (moduleId) => {
    setLocalActiveModule(moduleId);
  };

  return (
    <div style={{ display: "flex" }}>
      <Sidebar 
        active={active}
        setActive={handleSetActive}
        activeModule={localActiveModule || activeModule}
        setActiveModule={handleSetActiveModule}
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />
      <div style={{ 
        marginLeft: collapsed ? 80 : 280, 
        transition: "margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        flex: 1,
        minHeight: "100vh",
        background: `linear-gradient(135deg, ${COLORS.emerald50} 0%, ${COLORS.emerald100} 100%)`,
      }}>
        {/* Top Bar */}
        <div style={{
          height: 60,
          background: COLORS.blanc,
          borderBottom: `1px solid ${COLORS.emerald200}`,
          display: "flex",
          alignItems: "center",
          padding: "0 24px",
          justifyContent: "space-between",
          position: "sticky",
          top: 0,
          zIndex: 50,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13 }}>
            <span style={{ color: COLORS.emerald700, fontWeight: 600 }}>FermeGest</span>
            <span style={{ color: COLORS.emerald400 }}>/</span>
            <span style={{ color: COLORS.emerald500, fontWeight: 600 }}>{getTitle()}</span>
          </div>
          
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            {active !== "dashboard" && (
              <button
                onClick={() => setShowAddModal(true)}
                style={{
                  background: `linear-gradient(135deg, ${COLORS.emerald500}, ${COLORS.emerald600})`,
                  color: "#fff",
                  borderRadius: 8,
                  padding: "6px 16px",
                  fontSize: 12,
                  fontWeight: 600,
                  cursor: "pointer",
                  border: "none",
                  transition: "transform 0.2s",
                }}
                onMouseEnter={(e) => e.target.style.transform = "scale(1.05)"}
                onMouseLeave={(e) => e.target.style.transform = "scale(1)"}
              >
                + Nouveau
              </button>
            )}
            <button
              onClick={handleLogout}
              style={{
                background: "transparent",
                border: `1px solid ${COLORS.emerald200}`,
                borderRadius: 8,
                padding: "6px 16px",
                fontSize: 12,
                cursor: "pointer",
                color: COLORS.emerald600,
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                e.target.style.background = COLORS.emerald50;
                e.target.style.borderColor = COLORS.emerald500;
              }}
              onMouseLeave={(e) => {
                e.target.style.background = "transparent";
                e.target.style.borderColor = COLORS.emerald200;
              }}
            >
              Déconnexion
            </button>
            <div style={{
              width: 34, height: 34, borderRadius: "50%",
              background: COLORS.emerald100,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 14, cursor: "pointer",
              transition: "transform 0.2s",
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = "scale(1.1)"}
            onMouseLeave={(e) => e.currentTarget.style.transform = "scale(1)"}>
              🔔
            </div>
          </div>
        </div>

        {/* Contenu principal */}
        <div style={{ padding: 24 }}>
          {renderContent()}
        </div>
      </div>

      {/* Modal d'ajout */}
      {showAddModal && (
        <div style={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          background: "rgba(0,0,0,0.5)",
          backdropFilter: "blur(4px)",
          display: "flex", alignItems: "center", justifyContent: "center",
          zIndex: 1000,
        }} onClick={() => setShowAddModal(false)}>
          <div style={{
            background: COLORS.blanc, borderRadius: 16,
            width: "90%", maxWidth: 500, padding: 24,
          }} onClick={(e) => e.stopPropagation()}>
            <h2 style={{ color: COLORS.emerald700, marginBottom: 20 }}>Ajouter {getTitle()}</h2>
            <p style={{ color: COLORS.emerald600, marginBottom: 20 }}>
              Formulaire d'ajout pour {getTitle()} à implémenter...
            </p>
            <button
              onClick={() => setShowAddModal(false)}
              style={{
                width: "100%",
                background: COLORS.emerald500,
                color: "white",
                padding: "10px",
                border: "none",
                borderRadius: 8,
                cursor: "pointer"
              }}
            >
              Fermer
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardLayout;