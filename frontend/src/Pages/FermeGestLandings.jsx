import { useState, useEffect, useRef } from "react";

export default function FermeGestLandings() {
  const [showLogin, setShowLogin] = useState(false);
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [loginError, setLoginError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [activeSection, setActiveSection] = useState("accueil");
  const [isScrolled, setIsScrolled] = useState(false);
  const [isNearTop, setIsNearTop] = useState(true);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [modalClosing, setModalClosing] = useState(false);
  const [modalOpening, setModalOpening] = useState(false);
  
  const sectionsRef = useRef({});
  const accueilRef = useRef(null);
  const servicesRef = useRef(null);
  const fonctionnalitesRef = useRef(null);
  const contactRef = useRef(null);

  // Images spécifiques pour chaque type d'élevage
  const farmImages = [
    {
      url: "https://images.unsplash.com/photo-1546443049-6d6a36b0a8a6?w=1200&h=600&fit=crop",
      alt: "Troupeau de bovins dans un pré",
      caption: "Élevage Bovin",
      description: "Gestion complète du cheptel bovin",
      type: "bovin"
    },
    {
      url: "https://images.unsplash.com/photo-1516467506338-6bd5f3c6b3d8?w=1200&h=600&fit=crop",
      alt: "Porc dans un élevage moderne",
      caption: "Élevage Porcin",
      description: "Suivi de reproduction et croissance",
      type: "porcin"
    },
    {
      url: "https://images.unsplash.com/photo-1566577134502-8be61c6e5e6b?w=1200&h=600&fit=crop",
      alt: "Poules dans un élevage avicole",
      caption: "Élevage Avicole - Poulaille",
      description: "Gestion des poules pondeuses et poulets de chair",
      type: "poulaille"
    },
    {
      url: "https://images.unsplash.com/photo-1576201689981-fc297238c2b6?w=1200&h=600&fit=crop",
      alt: "Moutons dans un pâturage",
      caption: "Élevage Ovin",
      description: "Suivi sanitaire et production lainière",
      type: "ovin"
    },
    {
      url: "https://images.unsplash.com/photo-1591277939652-8ff6f224b4f9?w=1200&h=600&fit=crop",
      alt: "Chèvres en liberté",
      caption: "Élevage Caprin",
      description: "Gestion des troupeaux caprins",
      type: "caprin"
    },
    {
      url: "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=1200&h=600&fit=crop",
      alt: "Canards dans une ferme",
      caption: "Élevage de Canards",
      description: "Production et santé avicole",
      type: "canard"
    }
  ];

  // Vérifier si l'utilisateur est authentifié
  const isAuthenticated = () => {
    const token = localStorage.getItem("token");
    return token !== null;
  };

  // Empêcher le retour au dashboard avec la flèche du navigateur
  const preventBackToDashboard = () => {
    // Vérifier si on vient du dashboard (via l'historique)
    const previousPage = document.referrer;
    
    if (!isAuthenticated() && previousPage.includes('/sidebar')) {
      // Ajouter un état dans l'historique pour bloquer le retour
      window.history.pushState(null, '', window.location.href);
      
      // Gérer l'événement popstate (clic sur flèche retour)
      const handlePopState = () => {
        // Rediriger vers la page actuelle ou recharger
        window.location.href = '/';
        // Alternative: window.location.reload();
      };
      
      window.addEventListener('popstate', handlePopState);
      
      // Nettoyage
      return () => {
        window.removeEventListener('popstate', handlePopState);
      };
    }
  };

  useEffect(() => {
    sectionsRef.current = {
      accueil: accueilRef.current,
      services: servicesRef.current,
      fonctionnalites: fonctionnalitesRef.current,
      contact: contactRef.current,
    };
  }, []);

  // Gestion de la flèche de navigation
  useEffect(() => {
    // Appliquer la prévention du retour au dashboard
    const cleanup = preventBackToDashboard();
    
    // Nettoyer l'event listener au démontage du composant
    return () => {
      if (cleanup) cleanup();
    };
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      setIsScrolled(scrollY > 50);
      setIsNearTop(scrollY < 100);
      
      const scrollPosition = scrollY + 100;
      for (const [key, ref] of Object.entries(sectionsRef.current)) {
        if (ref) {
          const offsetTop = ref.offsetTop;
          const offsetBottom = offsetTop + ref.offsetHeight;
          if (scrollPosition >= offsetTop && scrollPosition < offsetBottom) {
            setActiveSection(key);
            break;
          }
        }
      }
    };
    
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Carrousel automatique toutes les 6 secondes
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % farmImages.length);
    }, 6000);
    
    return () => clearInterval(interval);
  }, []);

  // FONCTION CORRIGÉE - Navigation fluide
  const scrollToSection = (sectionId) => {
    const section = sectionsRef.current[sectionId];
    if (section) {
      const offset = 70; // Ajustement pour la hauteur du header fixe
      const elementPosition = section.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth"
      });
      setActiveSection(sectionId);
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const scrollToBottom = () => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
  };

  const handleOpenModal = () => {
    setModalClosing(false);
    setModalOpening(true);
    setShowLogin(true);
    setTimeout(() => {
      setModalOpening(false);
    }, 300);
  };

  const handleCloseModal = () => {
    setModalClosing(true);
    setTimeout(() => {
      setShowLogin(false);
      setModalClosing(false);
    }, 300);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!loginForm.email || !loginForm.password) {
      setLoginError("Veuillez remplir tous les champs");
      return;
    }

    setIsLoading(true);
    setLoginError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          login: loginForm.email,
          password: loginForm.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        // Nettoyer l'historique avant la redirection
        window.history.replaceState(null, '', '/dashboard');
        window.location.href = "/dashboard";
      } else {
        setLoginError(data.error || "Identifiant ou mot de passe incorrect");
      }
    } catch (error) {
      setLoginError("Impossible de contacter le serveur", error);
    } finally {
      setIsLoading(false);
    }
  };

  const navItems = [
    { id: "accueil", label: "Accueil" },
    { id: "services", label: "Services" },
    { id: "fonctionnalites", label: "Fonctionnalités" },
  ];

  const services = [
    { title: "Gestion d'élevage", description: "Suivi complet du cheptel, gestion des naissances et reproduction" },
    { title: "Production agricole", description: "Planification des cultures et suivi des récoltes" },
    { title: "Gestion des stocks", description: "Inventaire en temps réel et alertes de seuil" },
    { title: "Ventes & Finance", description: "Facturation et rapports financiers détaillés" },
    { title: "Santé animale", description: "Carnet sanitaire et rappels vaccins" },
    { title: "Analyses & Rapports", description: "Tableaux de bord personnalisés et KPIs" },
  ];

  const fonctionnalites = [
    { title: "Animaux", stat: "142 actifs" },
    { title: "Productions", stat: "284 L/jour" },
    { title: "Alimentation", stat: "8 aliments" },
    { title: "Santé", stat: "0 urgence" },
    { title: "Stocks", stat: "12 réf." },
    { title: "Ventes", stat: "4,8M Ar" },
    { title: "Engrais", stat: "1,2T/mois" },
    { title: "Reproduction", stat: "3 ce mois" },
  ];

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50/30 to-green-50">
      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        isScrolled ? "bg-white/95 backdrop-blur-md shadow-lg" : "bg-white/80 backdrop-blur-sm"
      }`}>
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-14 max-w-[1400px] mx-auto">
            <div className="flex items-center space-x-2 cursor-pointer group" onClick={() => scrollToSection("accueil")}>
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl shadow-md group-hover:scale-110 transition-transform duration-300" />
              <span className="text-lg font-bold bg-gradient-to-r from-emerald-700 to-green-600 bg-clip-text text-transparent">
                Ferme Fianar
              </span>
            </div>

            <div className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => scrollToSection(item.id)}
                  className={`px-4 py-2 rounded-xl transition-all duration-300 text-sm font-medium ${
                    activeSection === item.id
                      ? "bg-emerald-100 text-emerald-700 shadow-sm"
                      : "text-gray-600 hover:bg-emerald-50 hover:text-emerald-600"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <button
              onClick={handleOpenModal}
              className="px-5 py-2 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 transition-all duration-300 shadow-md hover:shadow-lg text-sm font-medium transform hover:scale-105"
            >
              Connexion
            </button>
          </div>
        </div>
      </nav>

      <div className="h-1" />

      {/* Hero Section */}
      <section ref={accueilRef} id="accueil" className="relative w-full overflow-hidden py-20 lg:py-24">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-100/20 via-teal-50/10 to-transparent pointer-events-none" />
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="max-w-[1400px] mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="space-y-6 animate-fade-in-up">
                <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 rounded-full text-emerald-700 text-xs font-medium shadow-sm">
                  <div className="w-1.5 h-1.5 bg-emerald-600 rounded-full animate-pulse mb-3" />
                  Gestion agricole intelligente
                </div>
                <h1 className="text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 leading-tight">
                  Votre ferme,{" "}
                  <span className="bg-gradient-to-r from-emerald-600 to-green-500 bg-clip-text text-transparent block mt-3">
                    entièrement maîtrisée
                  </span>
                </h1>
                <p className="text-gray-600 leading-relaxed text-base lg:text-lg max-w-xl">
                  FermeGest centralise la gestion de vos animaux, productions, stocks et ventes.
                  Conçu pour les éleveurs de Fianarantsoa.
                </p>
                <div className="flex flex-wrap gap-4">
                  <button
                    onClick={handleOpenModal}
                    className="px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 transition-all duration-300 shadow-md hover:shadow-lg text-sm font-medium transform hover:scale-105"
                  >
                    Commencer
                  </button>
                  <button 
                    onClick={() => scrollToSection("services")}
                    className="px-8 py-3 border-2 border-emerald-300 text-emerald-700 rounded-xl hover:border-emerald-600 hover:text-emerald-600 hover:bg-emerald-50 transition-all duration-300 text-sm font-medium transform hover:scale-105"
                  >
                    Découvrir
                  </button>
                </div>

                <div className="flex gap-10 pt-6">
                  <div className="group cursor-pointer">
                    <div className="text-3xl lg:text-4xl font-bold text-gray-900 group-hover:text-emerald-600 transition-colors duration-300">142+</div>
                    <div className="text-xs text-gray-500">Animaux</div>
                  </div>
                  <div className="group cursor-pointer">
                    <div className="text-3xl lg:text-4xl font-bold text-gray-900 group-hover:text-emerald-600 transition-colors duration-300">284L</div>
                    <div className="text-xs text-gray-500">Lait/jour</div>
                  </div>
                  <div className="group cursor-pointer">
                    <div className="text-3xl lg:text-4xl font-bold text-gray-900 group-hover:text-emerald-600 transition-colors duration-300">98%</div>
                    <div className="text-xs text-gray-500">Santé</div>
                  </div>
                </div>
              </div>

              {/* Carrousel d'images agricoles */}
              <div className="relative group">
                <div className="rounded-2xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105">
                  <div className="relative w-full h-[400px] lg:h-[500px] xl:h-[550px]">
                    {farmImages.map((image, index) => (
                      <div
                        key={index}
                        className={`absolute inset-0 transition-all duration-1000 ease-in-out ${
                          index === currentImageIndex 
                            ? "opacity-100 transform scale-100" 
                            : "opacity-0 transform scale-110"
                        }`}
                      >
                        <img
                          src={image.url}
                          alt={image.alt}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-6">
                          <p className="text-white text-xl lg:text-2xl font-bold mb-2 animate-fade-in-up">
                            {image.caption}
                          </p>
                          <p className="text-white/90 text-sm lg:text-base animate-fade-in-up">
                            {image.description}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                {/* Indicateurs du carrousel */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 z-10">
                  {farmImages.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentImageIndex(index)}
                      className={`transition-all duration-300 rounded-full ${
                        index === currentImageIndex
                          ? "w-8 h-2 bg-emerald-500"
                          : "w-2 h-2 bg-white/50 hover:bg-white/80"
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section - Cartes flottantes */}
      <section ref={servicesRef} id="services" className="w-full py-20 lg:py-24 bg-white/40 backdrop-blur-sm">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="max-w-[1400px] mx-auto">
            <div className="text-center mb-12 animate-fade-in-up">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-100 rounded-full text-emerald-700 text-xs font-medium mb-4 shadow-sm">
                Nos services
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-3">
                Solutions pour votre exploitation
              </h2>
              <p className="text-gray-600 text-sm max-w-xl mx-auto">
                Des services complets pour optimiser la gestion de votre ferme
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((service, i) => (
                <div
                  key={i}
                  className="bg-white/90 backdrop-blur-sm rounded-2xl border border-emerald-200 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 overflow-hidden animate-float-card group"
                  style={{ animationDelay: `${i * 0.2}s` }}
                >
                  <div className="h-1.5 bg-gradient-to-r from-emerald-400 to-green-600 group-hover:h-2 transition-all duration-300" />
                  <div className="p-7">
                    <h3 className="text-xl lg:text-2xl font-semibold text-gray-900 mb-3 group-hover:text-emerald-600 transition-colors duration-300">
                      {service.title}
                    </h3>
                    <p className="text-sm text-gray-500 leading-relaxed">{service.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Fonctionnalités Section */}
      <section ref={fonctionnalitesRef} id="fonctionnalites" className="w-full py-20 lg:py-24 bg-gradient-to-br from-emerald-100/30 via-teal-50/20 to-green-100/30">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="max-w-[1400px] mx-auto">
            <div className="text-center mb-12 animate-fade-in-up">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-200 rounded-full text-emerald-700 text-xs font-medium mb-4 shadow-sm">
                Fonctionnalités
              </div>
              <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-3">
                8 modules intégrés
              </h2>
              <p className="text-gray-600 text-sm">Pour une gestion complète de votre exploitation</p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {fonctionnalites.map((feature, i) => (
                <div
                  key={i}
                  className="bg-white/90 backdrop-blur-sm rounded-2xl border border-emerald-200 shadow-md hover:shadow-xl transition-all duration-500 hover:-translate-y-2 cursor-pointer p-6 animate-float-card-light group"
                  style={{ animationDelay: `${i * 0.1}s` }}
                >
                  <div className="mb-3">
                    <div className="text-2xl lg:text-3xl font-bold text-gray-800 group-hover:text-emerald-600 transition-colors duration-300">
                      {feature.stat}
                    </div>
                  </div>
                  <h3 className="text-base font-semibold text-gray-700 group-hover:text-emerald-600 transition-colors duration-300">{feature.title}</h3>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer - Vert doux */}
      <footer className="w-full bg-gradient-to-br from-emerald-100 to-green-100 border-t border-emerald-200 py-8">
        <div className="w-full px-4 sm:px-6 lg:px-8">
          <div className="max-w-[1400px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg shadow-sm" />
              <span className="text-sm font-semibold text-gray-700">FermeGest</span>
              <span className="text-xs text-gray-500">© 2025</span>
            </div>
            <div className="flex gap-6 text-xs">
              {navItems.map((item) => (
                <button key={item.id} onClick={() => scrollToSection(item.id)} className="text-gray-600 hover:text-emerald-600 transition-colors duration-300 font-medium">
                  {item.label}
                </button>
              ))}
            </div>
            <div className="text-xs text-gray-500">Fianarantsoa, Madagascar</div>
          </div>
        </div>
      </footer>

      {/* Modal Connexion fluide */}
      {showLogin && (
        <div 
          className={`fixed inset-0 bg-black/50 backdrop-blur-md z-50 flex items-center justify-center p-4 transition-all duration-500 ease-out ${
            modalClosing ? "opacity-0" : "opacity-100"
          } ${modalOpening ? "animate-fade-in" : ""}`}
          onClick={handleCloseModal}
        >
          <div 
            className={`bg-white rounded-2xl max-w-md w-full p-6 transform transition-all duration-500 ease-out ${
              modalClosing ? "scale-95 opacity-0 translate-y-4" : "scale-100 opacity-100 translate-y-0"
            } ${modalOpening ? "animate-modal-in" : ""}`}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-5">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl" />
                <h2 className="text-xl font-bold text-gray-800">Connexion</h2>
              </div>
              <button 
                onClick={handleCloseModal} 
                className="text-gray-400 hover:text-gray-600 text-2xl transition-all duration-300 hover:rotate-90 hover:scale-110"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Identifiant</label>
                <input
                  type="text"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition-all duration-300"
                  placeholder="Entrez votre identifiant"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Mot de passe</label>
                <input
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition-all duration-300"
                  placeholder="••••••••"
                />
              </div>

              {loginError && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-2 text-xs text-red-600 animate-shake">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-2.5 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-lg hover:from-emerald-600 hover:to-green-700 transition-all duration-300 text-sm font-medium disabled:opacity-50 transform hover:scale-105"
              >
                {isLoading ? "Connexion..." : "Se connecter"}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Bouton flèche dynamique */}
      <button
        onClick={isNearTop ? scrollToBottom : scrollToTop}
        className={`fixed bottom-4 right-4 w-12 h-12 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-500 flex items-center justify-center z-40 text-xl font-bold hover:scale-110 ${
          isScrolled ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10 pointer-events-none"
        }`}
      >
        {isNearTop ? "↓" : "↑"}
      </button>

      <style>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes scale-in {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
        
        @keyframes float-card {
          0%, 100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-8px);
          }
        }
        
        @keyframes float-card-light {
          0%, 100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-5px);
          }
        }
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
        
        @keyframes modal-in {
          from {
            opacity: 0;
            transform: scale(0.95) translateY(-20px);
          }
          to {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }
        
        .animate-fade-in-up {
          animation: fade-in-up 0.6s ease-out forwards;
        }
        
        .animate-scale-in {
          animation: scale-in 0.4s ease-out forwards;
        }
        
        .animate-float-card {
          animation: float-card 4s ease-in-out infinite;
        }
        
        .animate-float-card-light {
          animation: float-card-light 3s ease-in-out infinite;
        }
        
        .animate-shake {
          animation: shake 0.3s ease-in-out;
        }
        
        .animate-fade-in {
          animation: fade-in 0.3s ease-out forwards;
        }
        
        .animate-modal-in {
          animation: modal-in 0.4s cubic-bezier(0.34, 1.2, 0.64, 1) forwards;
        }
      `}</style>
    </div>
  );
}