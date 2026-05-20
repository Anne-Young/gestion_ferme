// Sidebar.jsx - Version modernisée sans warnings
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { COLORS, modules } from "./menuConfig";

function Sidebar({ active, setActive, activeModule, setActiveModule, collapsed, setCollapsed }) {
  const navigate = useNavigate();
  const [hoveredItem, setHoveredItem] = useState(null);

  const handleMenuClick = (module, submenuKey = null) => {
    if (module.isDirect) {
      setActive(module.key);
      setActiveModule(null);
      navigate(`/dashboard/${module.key}`);
    } else if (submenuKey) {
      setActive(submenuKey);
      setActiveModule(module.id);
      navigate(`/dashboard/${module.id}/${submenuKey}`);
    } else {
      setActiveModule(activeModule === module.id ? null : module.id);
    }
  };

  const isModuleActive = (moduleId) => activeModule === moduleId;
  const isDirectActive = (module) => module.isDirect && active === module.key;

  return (
    <div style={{
      width: collapsed ? 80 : 280,
      minHeight: "100vh",
      background: COLORS.gray[900],
      transition: "width 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
      display: "flex",
      flexDirection: "column",
      position: "fixed",
      left: 0, top: 0, bottom: 0,
      zIndex: 100,
      overflowY: "auto",
      overflowX: "hidden",
      boxShadow: "4px 0 20px rgba(0,0,0,0.1)",
    }}>
      {/* Header avec logo */}
      <div style={{
        padding: collapsed ? "20px 0" : "24px 20px",
        borderBottom: `1px solid ${COLORS.gray[700]}`,
        display: "flex",
        alignItems: "center",
        justifyContent: collapsed ? "center" : "space-between",
        gap: 12,
        flexShrink: 0,
      }}>
        <div style={{
          width: 40, height: 40, borderRadius: 12,
          background: `linear-gradient(135deg, ${COLORS.primary.main}, ${COLORS.primary.light})`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 20, flexShrink: 0,
          boxShadow: "0 4px 6px rgba(59, 130, 246, 0.2)",
        }}>🌿</div>
        {!collapsed && (
          <div style={{ flex: 1 }}>
            <div style={{ color: COLORS.blanc, fontWeight: 700, fontSize: 16 }}>FermeGest</div>
            <div style={{ color: COLORS.gray[400], fontSize: 11 }}>Gestion agricole</div>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          style={{
            background: COLORS.gray[800],
            border: `1px solid ${COLORS.gray[700]}`,
            borderRadius: 8,
            width: 28, height: 28,
            display: "flex", alignItems: "center", justifyContent: "center",
            cursor: "pointer",
            color: COLORS.gray[400],
            fontSize: 16,
            transition: "all 0.2s",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = COLORS.gray[700];
            e.currentTarget.style.color = COLORS.primary.light;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = COLORS.gray[800];
            e.currentTarget.style.color = COLORS.gray[400];
          }}
        >
          {collapsed ? "→" : "←"}
        </button>
      </div>

      {/* Liste des menus */}
      <div style={{ flex: 1, padding: "20px 12px" }}>
        {modules.map((module) => {
          const moduleActive = isModuleActive(module.id);
          const directActive = isDirectActive(module);
          const showSubmenus = moduleActive && module.submenus && !collapsed;
          const isHovered = hoveredItem === module.id;
          
          return (
            <div key={module.id} style={{ marginBottom: 8 }}>
              <button
                onClick={() => handleMenuClick(module)}
                onMouseEnter={() => setHoveredItem(module.id)}
                onMouseLeave={() => setHoveredItem(null)}
                style={{
                  display: "flex", alignItems: "center", gap: 12,
                  padding: collapsed ? "12px 0" : "12px 16px",
                  justifyContent: collapsed ? "center" : "flex-start",
                  cursor: "pointer",
                  background: (moduleActive || directActive) 
                    ? COLORS.active.bg 
                    : isHovered 
                      ? COLORS.gray[800] 
                      : "transparent",
                  borderRadius: 12,
                  width: "100%",
                  border: "none",
                  color: (moduleActive || directActive) 
                    ? COLORS.active.text 
                    : isHovered 
                      ? COLORS.blanc 
                      : COLORS.gray[400],
                  transition: "all 0.2s ease",
                  position: "relative",
                }}
              >
                <span style={{ fontSize: 18 }}>{module.icon}</span>
                {!collapsed && (
                  <>
                    <span style={{
                      fontSize: 13,
                      fontWeight: (moduleActive || directActive) ? 600 : 400,
                      flex: 1,
                      textAlign: "left",
                    }}>
                      {module.label}
                    </span>
                    {module.submenus && (
                      <span style={{
                        fontSize: 11,
                        transform: showSubmenus ? "rotate(180deg)" : "rotate(0deg)",
                        transition: "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                      }}>▼</span>
                    )}
                  </>
                )}
                {(moduleActive || directActive) && !collapsed && (
                  <div style={{
                    position: "absolute",
                    left: 0,
                    top: "50%",
                    transform: "translateY(-50%)",
                    width: 3,
                    height: 20,
                    background: COLORS.primary.main,
                    borderRadius: "0 2px 2px 0",
                  }} />
                )}
              </button>

              {/* Sous-menus */}
              {module.submenus && (
                <div style={{
                  marginLeft: collapsed ? 0 : 32,
                  marginTop: showSubmenus ? 8 : 0,
                  marginBottom: showSubmenus ? 8 : 0,
                  maxHeight: showSubmenus ? 500 : 0,
                  opacity: showSubmenus ? 1 : 0,
                  overflow: "hidden",
                  transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                  pointerEvents: showSubmenus ? "auto" : "none",
                }}>
                  {module.submenus.map((submenu) => (
                    <button
                      key={submenu.key}
                      onClick={() => handleMenuClick(module, submenu.key)}
                      onMouseEnter={() => setHoveredItem(`${module.id}-${submenu.key}`)}
                      onMouseLeave={() => setHoveredItem(null)}
                      style={{
                        display: "flex", alignItems: "center", gap: 10,
                        padding: "10px 12px",
                        cursor: "pointer",
                        background: active === submenu.key 
                          ? COLORS.active.bg 
                          : hoveredItem === `${module.id}-${submenu.key}`
                            ? COLORS.gray[800]
                            : "transparent",
                        borderRadius: 8,
                        width: "100%",
                        border: "none",
                        marginBottom: 4,
                        transition: "all 0.15s ease",
                        position: "relative",
                      }}
                    >
                      <span style={{ fontSize: 14 }}>{submenu.icon}</span>
                      {!collapsed && (
                        <span style={{
                          fontSize: 12,
                          fontWeight: active === submenu.key ? 500 : 400,
                          color: active === submenu.key 
                            ? COLORS.active.text 
                            : hoveredItem === `${module.id}-${submenu.key}`
                              ? COLORS.blanc
                              : COLORS.gray[400],
                        }}>
                          {submenu.label}
                        </span>
                      )}
                      {active === submenu.key && !collapsed && (
                        <div style={{
                          position: "absolute",
                          left: 0,
                          top: "50%",
                          transform: "translateY(-50%)",
                          width: 3,
                          height: 16,
                          background: COLORS.primary.main,
                          borderRadius: "0 2px 2px 0",
                        }} />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

     
    </div>
  );
}

export default Sidebar;