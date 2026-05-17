import { useState, useEffect, useRef } from "react";

/* ── Fonts & Global Styles ── */
const GlobalStyles = () => (
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; font-size: 16px; }
    body { font-family: 'Outfit', sans-serif; background: #0A1205; color: #E8F0DC; overflow-x: hidden; }

    :root {
      --green-950: #050B02;
      --green-900: #0A1205;
      --green-800: #122108;
      --green-700: #1C3410;
      --green-600: #274D18;
      --green-500: #3B6D11;
      --green-400: #639922;
      --green-300: #97C459;
      --green-200: #C0DD97;
      --green-100: #EAF3DE;
      --gold-400: #D4A843;
      --gold-300: #E8C574;
      --gold-200: #F2DFA8;
      --cream: #F5F0E8;
      --text-primary: #E8F0DC;
      --text-muted: #8FA87A;
      --border: rgba(151,196,89,0.15);
      --border-bright: rgba(151,196,89,0.35);
    }

    ::selection { background: var(--green-400); color: #fff; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--green-900); }
    ::-webkit-scrollbar-thumb { background: var(--green-500); border-radius: 3px; }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(32px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes scaleIn {
      from { opacity: 0; transform: scale(0.92); }
      to   { opacity: 1; transform: scale(1); }
    }
    @keyframes shimmer {
      0%   { background-position: -200% center; }
      100% { background-position: 200% center; }
    }
    @keyframes pulse-ring {
      0%   { transform: scale(1); opacity: 0.6; }
      100% { transform: scale(1.6); opacity: 0; }
    }
    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50%       { transform: translateY(-10px); }
    }
    @keyframes rotateSlow {
      from { transform: rotate(0deg); }
      to   { transform: rotate(360deg); }
    }
    @keyframes grain {
      0%, 100% { transform: translate(0, 0); }
      10%  { transform: translate(-2%, -3%); }
      30%  { transform: translate(3%, -1%); }
      50%  { transform: translate(-1%, 2%); }
      70%  { transform: translate(2%, 3%); }
      90%  { transform: translate(-3%, 1%); }
    }

    .reveal { opacity: 0; transform: translateY(28px); transition: opacity 0.7s ease, transform 0.7s ease; }
    .reveal.visible { opacity: 1; transform: translateY(0); }

    .nav-pill {
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-muted);
      background: none;
      border: none;
      padding: 7px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: color 0.2s, background 0.2s;
      letter-spacing: 0.2px;
    }
    .nav-pill:hover { color: var(--green-200); background: rgba(151,196,89,0.08); }
    .nav-pill.active { color: var(--green-300); background: rgba(151,196,89,0.12); }

    .btn-primary {
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 600;
      background: var(--green-400);
      color: #fff;
      border: none;
      padding: 11px 24px;
      border-radius: 100px;
      cursor: pointer;
      letter-spacing: 0.3px;
      transition: all 0.25s;
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }
    .btn-primary:hover { background: var(--green-300); color: var(--green-900); transform: translateY(-1px); box-shadow: 0 8px 24px rgba(99,153,34,0.35); }

    .btn-ghost {
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 500;
      background: transparent;
      color: var(--text-muted);
      border: 1px solid var(--border);
      padding: 10px 22px;
      border-radius: 100px;
      cursor: pointer;
      transition: all 0.25s;
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }
    .btn-ghost:hover { border-color: var(--border-bright); color: var(--green-200); }

    .input-field {
      width: 100%;
      background: rgba(151,196,89,0.05);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 16px;
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      color: var(--text-primary);
      outline: none;
      transition: border-color 0.2s, background 0.2s;
    }
    .input-field::placeholder { color: var(--text-muted); }
    .input-field:focus { border-color: var(--green-400); background: rgba(151,196,89,0.08); }

    .card-glass {
      background: rgba(18, 33, 8, 0.6);
      border: 1px solid var(--border);
      border-radius: 20px;
      backdrop-filter: blur(12px);
      transition: border-color 0.3s, transform 0.3s;
    }
    .card-glass:hover { border-color: var(--border-bright); transform: translateY(-3px); }

    .section-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--green-400);
      background: rgba(99,153,34,0.1);
      border: 1px solid rgba(99,153,34,0.2);
      border-radius: 100px;
      padding: 5px 14px;
      margin-bottom: 1.2rem;
    }

    .shimmer-text {
      background: linear-gradient(90deg, var(--green-200) 0%, var(--gold-300) 30%, var(--green-300) 60%, var(--gold-300) 80%, var(--green-200) 100%);
      background-size: 200% auto;
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: shimmer 4s linear infinite;
    }

    .modal-backdrop {
      position: fixed; inset: 0;
      background: rgba(5, 11, 2, 0.85);
      backdrop-filter: blur(8px);
      z-index: 1000;
      display: flex; align-items: center; justify-content: center;
      animation: fadeIn 0.2s ease;
      padding: 1rem;
    }
    .modal-box {
      background: var(--green-800);
      border: 1px solid var(--border-bright);
      border-radius: 24px;
      width: 100%;
      max-width: 420px;
      padding: 2.5rem;
      position: relative;
      animation: scaleIn 0.3s ease;
    }

    .accordion-btn {
      width: 100%; background: none; border: none;
      padding: 18px 0; text-align: left;
      font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 500;
      color: var(--text-primary); cursor: pointer;
      display: flex; justify-content: space-between; align-items: center;
      transition: color 0.2s;
    }
    .accordion-btn:hover { color: var(--green-300); }

    .security-badge {
      display: flex; align-items: center; gap: 10px;
      background: rgba(18,33,8,0.7);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px 16px;
      transition: border-color 0.2s;
    }
    .security-badge:hover { border-color: var(--border-bright); }

    .footer-link { color: var(--text-muted); font-size: 13px; cursor: pointer; transition: color 0.2s; text-decoration: none; }
    .footer-link:hover { color: var(--green-300); }

    .grain-overlay {
      position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: 0.025;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
      animation: grain 0.5s steps(2) infinite;
    }
  `}</style>
);

/* ── Data ── */
const MODULES = [
  { icon: "🐄", titre: "Gestion des animaux", desc: "Suivi complet par espèce, race, enclos et statut. Historique individuel de chaque tête de bétail.", stat: "142 actifs", color: "var(--green-400)" },
  { icon: "🥛", titre: "Productions", desc: "Collecte quotidienne lait, œufs et viande avec grades de qualité A/B/C et traçabilité complète.", stat: "284 L/jour", color: "#5DCAA5" },
  { icon: "🌾", titre: "Alimentation", desc: "Rations individuelles ou groupées par enclos, avec déduction automatique des stocks fourrages.", stat: "8 aliments", color: "var(--gold-400)" },
  { icon: "💊", titre: "Santé animale", desc: "Vaccinations, traitements vétérinaires et rappels automatiques de rendez-vous programmés.", stat: "0 urgence", color: "#85B7EB" },
  { icon: "📦", titre: "Stocks", desc: "Alertes seuil critique sur aliments et produits finis. Vision en temps réel des inventaires.", stat: "12 réf.", color: "#F09595" },
  { icon: "💰", titre: "Ventes & CA", desc: "Enregistrement des ventes en Ariary, suivi acheteurs et rapports de chiffre d'affaires.", stat: "4,8M MGA", color: "var(--gold-300)" },
  { icon: "🌿", titre: "Engrais & Compost", desc: "Cycle complet de valorisation du fumier — collecte, compostage, traitement et revente.", stat: "1,2T/mois", color: "#97C459" },
  { icon: "🐣", titre: "Reproduction", desc: "Suivi des saillies, naissances, taux de survie et génétique des portées.", stat: "3 ce mois", color: "#ED93B1" },
];

const SECURITY_ITEMS = [
  { icon: "🔐", titre: "Mots de passe chiffrés", desc: "Hachage bcrypt irréversible — aucun mot de passe n'est stocké en clair." },
  { icon: "👤", titre: "Contrôle d'accès RBAC", desc: "Trois niveaux : Administrateur, Gérant, Employé — chaque rôle voit uniquement ce dont il a besoin." },
  { icon: "🛡️", titre: "Sessions sécurisées", desc: "Tokens JWT avec expiration automatique et renouvellement contrôlé." },
  { icon: "📋", titre: "Journaux d'activité", desc: "Toutes les actions critiques sont tracées avec horodatage et identité de l'opérateur." },
  { icon: "🔒", titre: "Données locales", desc: "Vos données restent dans votre infrastructure. Aucune donnée transmise à des tiers." },
  { icon: "♻️", titre: "Sauvegardes automatiques", desc: "Snapshots quotidiens avec restauration possible en moins de 5 minutes." },
];

const FAQ_ITEMS = [
  { q: "Qui peut utiliser FermeGest ?", r: "Tout le personnel de la ferme selon son rôle — administrateurs pour la configuration, gérants pour le suivi global, employés pour les saisies quotidiennes. Chaque compte est créé et géré par l'administrateur de la ferme." },
  { q: "Le système fonctionne-t-il hors connexion ?", r: "La version actuelle nécessite Internet pour synchroniser. Une version hors ligne avec synchronisation différée est prévue pour la prochaine mise à jour majeure." },
  { q: "Comment sont calculés les stocks automatiquement ?", r: "Chaque distribution alimentaire déduit le stock correspondant. Chaque vente déduit le stock produit. Des alertes s'affichent dès qu'un seuil critique est atteint." },
  { q: "Peut-on générer des rapports ?", r: "Oui — rapports hebdomadaires et mensuels pour les productions, les ventes, le chiffre d'affaires par type de produit et les coûts vétérinaires par animal." },
  { q: "Comment réinitialiser un mot de passe ?", r: "Seul l'administrateur peut réinitialiser les accès depuis le panneau de gestion des utilisateurs. Aucune réinitialisation par email n'est nécessaire dans un environnement fermé." },
];

const TEAM = [
  { initiales: "RF", nom: "Rakoto Fidy", role: "Fondateur & Gérant", avatar: "var(--green-700)" },
  { initiales: "MV", nom: "Mavo Vola", role: "Responsable élevage", avatar: "var(--green-600)" },
  { initiales: "HA", nom: "Hery Andriantsoa", role: "Vétérinaire attitré", avatar: "#0F6E56" },
];

/* ── Modal Connexion ── */
function LoginModal({ onClose }) {
  const [tab, setTab] = useState("login");
  const [form, setForm] = useState({ login: "", password: "", nom: "", role: "employe" });
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [showPass, setShowPass] = useState(false);

 const handleSubmit = async () => {

  if (!form.login.trim() || !form.password.trim()) {
    setStatus({
      ok: false,
      msg: "Veuillez remplir tous les champs obligatoires."
    });
    return;
  }

  setLoading(true);
  setStatus(null);

  try {

    let url = "";
    let bodyData = {};

    // ───────── CONNEXION ─────────
    if (tab === "login") {

      url = "http://127.0.0.1:8000/api/auth/login/";

      bodyData = {
        login: form.login,
        password: form.password,
      };

    }

    // ───────── INSCRIPTION ─────────
    else {

      url = "http://127.0.0.1:8000/api/utilisateurs/create/";

      bodyData = {
        nom_complet: form.nom,
        login: form.login,
        password: form.password,
        role: form.role,
      };

    }

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bodyData),
    });

    const data = await response.json();

    if (response.ok) {

      setStatus({
        ok: true,
        msg:
          tab === "login"
            ? "Connexion réussie !"
            : "Compte créé avec succès !",
      });

      console.log(data);

    } else {

      setStatus({
        ok: false,
        msg: data.error || "Une erreur est survenue.",
      });

    }

  } catch (error) {

    setStatus({
      ok: false,
      msg: "Impossible de contacter le serveur Django.",
    });

    console.error(error);

  } finally {

    setLoading(false);

  }

};

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        {/* Close */}
        <button onClick={onClose} style={{ position: "absolute", top: 18, right: 18, background: "rgba(151,196,89,0.1)", border: "1px solid var(--border)", borderRadius: "50%", width: 32, height: 32, cursor: "pointer", color: "var(--text-muted)", fontSize: 16, display: "flex", alignItems: "center", justifyContent: "center" }}>✕</button>

        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: "1.8rem" }}>
          <div style={{ width: 52, height: 52, borderRadius: "50%", background: "rgba(99,153,34,0.15)", border: "1px solid rgba(99,153,34,0.3)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, margin: "0 auto 12px" }}>🌾</div>
          <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.6rem", fontWeight: 600, color: "var(--text-primary)", marginBottom: 4 }}>
            {tab === "login" ? "Accès à votre espace" : "Créer un compte"}
          </h2>
          <p style={{ fontSize: 13, color: "var(--text-muted)" }}>FermeGest · Fianarantsoa, Madagascar</p>
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", background: "rgba(0,0,0,0.2)", borderRadius: 12, padding: 4, marginBottom: "1.5rem", border: "1px solid var(--border)" }}>
          {[["login","🔐 Connexion"], ["register","✨ Inscription"]].map(([t, l]) => (
            <button key={t} onClick={() => { setTab(t); setStatus(null); }} style={{
              flex: 1, padding: "9px 0", border: "none", borderRadius: 9, cursor: "pointer",
              fontFamily: "'Outfit', sans-serif", fontSize: 13, fontWeight: 500,
              background: tab === t ? "var(--green-700)" : "transparent",
              color: tab === t ? "var(--green-200)" : "var(--text-muted)",
              transition: "all 0.2s",
            }}>{l}</button>
          ))}
        </div>

        {/* Form */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {tab === "register" && (
            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", letterSpacing: "1px", textTransform: "uppercase", display: "block", marginBottom: 6 }}>Nom complet</label>
              <input className="input-field" placeholder="Ex : Rakoto Jean" value={form.nom} onChange={e => setForm({ ...form, nom: e.target.value })} />
            </div>
          )}
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", letterSpacing: "1px", textTransform: "uppercase", display: "block", marginBottom: 6 }}>Identifiant</label>
            <input className="input-field" placeholder="Ex : rakoto.jean" value={form.login} onChange={e => setForm({ ...form, login: e.target.value })} />
          </div>
          <div>
            <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", letterSpacing: "1px", textTransform: "uppercase", display: "block", marginBottom: 6 }}>Mot de passe</label>
            <div style={{ position: "relative" }}>
              <input className="input-field" type={showPass ? "text" : "password"} placeholder="••••••••" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} style={{ paddingRight: 44 }} />
              <button onClick={() => setShowPass(!showPass)} style={{ position: "absolute", right: 12, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", color: "var(--text-muted)", cursor: "pointer", fontSize: 16 }}>
                {showPass ? "🙈" : "👁️"}
              </button>
            </div>
          </div>
          {tab === "register" && (
            <div>
              <label style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", letterSpacing: "1px", textTransform: "uppercase", display: "block", marginBottom: 6 }}>Rôle demandé</label>
              <select className="input-field" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })}>
                <option value="employe">👷 Employé</option>
                <option value="gerant">📋 Gérant</option>
                <option value="admin">⚙️ Administrateur</option>
              </select>
            </div>
          )}

          {tab === "login" && (
            <div style={{ textAlign: "right" }}>
              <span style={{ fontSize: 12, color: "var(--green-400)", cursor: "pointer", fontWeight: 500 }}>Mot de passe oublié ?</span>
            </div>
          )}

          {status && (
            <div style={{ padding: "10px 14px", borderRadius: 10, fontSize: 13, background: status.ok ? "rgba(99,153,34,0.12)" : "rgba(163,45,45,0.12)", color: status.ok ? "var(--green-300)" : "#F09595", border: `1px solid ${status.ok ? "rgba(99,153,34,0.25)" : "rgba(163,45,45,0.25)"}` }}>
              {status.msg}
            </div>
          )}

          <button className="btn-primary" onClick={handleSubmit} disabled={loading} style={{ width: "100%", justifyContent: "center", padding: "13px", fontSize: 15, marginTop: 4, opacity: loading ? 0.7 : 1 }}>
            {loading ? "⏳ Vérification…" : tab === "login" ? "Accéder au tableau de bord →" : "Envoyer la demande →"}
          </button>
        </div>

        <p style={{ fontSize: 11, color: "var(--text-muted)", textAlign: "center", marginTop: "1.2rem", lineHeight: 1.7 }}>
          En continuant, vous acceptez nos <span style={{ color: "var(--green-400)", cursor: "pointer" }}>Conditions d'utilisation</span> et notre <span style={{ color: "var(--green-400)", cursor: "pointer" }}>Politique de confidentialité</span>.
        </p>
      </div>
    </div>
  );
}

/* ── Main App ── */
export default function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState("accueil");
  const [openFaq, setOpenFaq] = useState(null);
  const [activePrivacy, setActivePrivacy] = useState("collecte");
  const revealRefs = useRef([]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) e.target.classList.add("visible"); });
    }, { threshold: 0.12 });
    revealRefs.current.forEach(el => el && obs.observe(el));
    return () => obs.disconnect();
  }, []);

  const addRef = el => { if (el && !revealRefs.current.includes(el)) revealRefs.current.push(el); };
  const goTo = id => { setActiveSection(id); document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }); };

  /* ── PRIVAte  Données*/
  const privacyData = {
    collecte: {
      titre: "Données collectées",
      contenu: "FermeGest collecte uniquement les données strictement nécessaires à son fonctionnement : informations d'identité des utilisateurs (nom, identifiant, rôle, téléphone), données zootechniques des animaux (numéro d'identification, race, espèce, statut, poids), historiques de production, de vente, d'alimentation, de santé animale et de reproduction. Aucune donnée personnelle sensible n'est collectée.",
      points: ["Identité et rôle des utilisateurs enregistrés", "Données d'identification des animaux", "Historiques de production, stock et ventes", "Actes vétérinaires et calendriers sanitaires", "Journaux d'activité système (logs horodatés)"],
    },
    utilisation: {
      titre: "Utilisation des données",
      contenu: "Les données collectées sont utilisées exclusivement pour faire fonctionner l'application de gestion agricole de la Ferme Fianarantsoa. Elles permettent de générer des tableaux de bord, des alertes automatiques, des rapports de production et des suivis vétérinaires.",
      points: ["Affichage des tableaux de bord et indicateurs", "Calcul automatique des stocks et alertes seuils", "Génération de rapports hebdomadaires et mensuels", "Rappels de rendez-vous vétérinaires", "Calcul du chiffre d'affaires et des coûts"],
    },
    droits: {
      titre: "Vos droits",
      contenu: "Chaque utilisateur de FermeGest dispose de droits relatifs à ses données personnelles. Ces droits peuvent être exercés en contactant directement l'administrateur de la ferme, qui dispose des outils pour y répondre depuis le panneau de gestion.",
      points: ["Droit d'accès : consulter les données vous concernant", "Droit de rectification : corriger des informations inexactes", "Droit à l'effacement : demander la suppression de votre compte", "Droit à la portabilité : exporter vos données en format lisible", "Droit d'opposition : refuser certains traitements de données"],
    },
  };
  const pc = privacyData[activePrivacy];

  return (
    <div style={{ background: "var(--green-900)", minHeight: "100vh", position: "relative" }}>
      <GlobalStyles />
      <div className="grain-overlay" />

      {/* NAVIGATION  */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 500,
        background: scrolled ? "rgba(10,18,5,0.92)" : "transparent",
        backdropFilter: scrolled ? "blur(20px)" : "none",
        borderBottom: scrolled ? "1px solid var(--border)" : "none",
        transition: "all 0.35s",
        height: 68,
        display: "flex", alignItems: "center",
        padding: "0 3rem",
        justifyContent: "space-between",
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 36, height: 36, borderRadius: "50%", background: "rgba(99,153,34,0.2)", border: "1px solid rgba(99,153,34,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17 }}>🌾</div>
          <div>
            <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.1rem", fontWeight: 700, color: "var(--green-200)", lineHeight: 1.1 }}>FermeGest</div>
            <div style={{ fontSize: 9, letterSpacing: "2px", textTransform: "uppercase", color: "var(--text-muted)" }}>Fianarantsoa · MG</div>
          </div>
        </div>

        {/* Links */}
        <div style={{ display: "flex", gap: 2, alignItems: "center" }}>
          {[["accueil","Accueil"],["modules","Modules"],["apropos","À propos"],["securite","Sécurité"],["faq","FAQ"],["confidentialite","Confidentialité"]].map(([id, label]) => (
            <button key={id} className={`nav-pill ${activeSection === id ? "active" : ""}`} onClick={() => goTo(id)}>{label}</button>
          ))}
        </div>

        {/* CTA */}
        <button className="btn-primary" onClick={() => setShowLogin(true)} style={{ fontSize: 13, padding: "9px 20px" }}>
          🔐 Connexion
        </button>
      </nav>

      {showLogin && <LoginModal onClose={() => setShowLogin(false)} />}

      {/*HERO */}
      <section id="accueil" style={{ position: "relative", minHeight: "100vh", display: "flex", alignItems: "center", overflow: "hidden", padding: "0 3rem" }}>

        {/* Ambient background */}
        <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse 80% 60% at 70% 50%, rgba(39,77,24,0.4) 0%, transparent 70%)" }} />
        <div style={{ position: "absolute", top: "15%", right: "8%", width: 380, height: 380, borderRadius: "50%", border: "1px solid rgba(151,196,89,0.08)", animation: "rotateSlow 30s linear infinite" }}>
          {[0,45,90,135,180,225,270,315].map(deg => (
            <div key={deg} style={{ position: "absolute", width: 6, height: 6, borderRadius: "50%", background: "rgba(151,196,89,0.35)", top: "50%", left: "50%", transform: `rotate(${deg}deg) translateX(189px) translateY(-50%)` }} />
          ))}
        </div>
        <div style={{ position: "absolute", top: "20%", right: "11%", width: 260, height: 260, borderRadius: "50%", border: "1px solid rgba(151,196,89,0.06)", animation: "rotateSlow 20s linear infinite reverse" }} />

        {/* Floating badge */}
        <div style={{ position: "absolute", right: "9%", top: "22%", animation: "float 5s ease-in-out infinite" }}>
          <div style={{ background: "rgba(18,33,8,0.85)", border: "1px solid rgba(151,196,89,0.25)", borderRadius: 16, padding: "16px 20px", backdropFilter: "blur(12px)", textAlign: "center" }}>
            <div style={{ fontSize: 28, marginBottom: 6 }}>📊</div>
            <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.6rem", fontWeight: 700, color: "var(--green-200)" }}>98%</div>
            <div style={{ fontSize: 11, color: "var(--text-muted)", letterSpacing: "0.5px" }}>Taux de santé</div>
          </div>
        </div>
        <div style={{ position: "absolute", right: "22%", top: "65%", animation: "float 6s ease-in-out infinite 1s" }}>
          <div style={{ background: "rgba(18,33,8,0.85)", border: "1px solid rgba(212,168,67,0.25)", borderRadius: 16, padding: "14px 18px", backdropFilter: "blur(12px)", textAlign: "center" }}>
            <div style={{ fontSize: 22, marginBottom: 4 }}>💰</div>
            <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.4rem", fontWeight: 700, color: "var(--gold-300)" }}>4,8M</div>
            <div style={{ fontSize: 11, color: "var(--text-muted)" }}>MGA / mois</div>
          </div>
        </div>

        {/* Hero content */}
        <div style={{ maxWidth: 640, position: "relative", zIndex: 1, paddingTop: 80 }}>
          <div style={{ animation: "fadeUp 0.8s ease both" }}>
            <span className="section-tag">🌍 Gestion agricole intelligente · Madagascar</span>
          </div>

          <h1 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(3rem, 5.5vw, 5rem)", fontWeight: 700, lineHeight: 1.08, marginBottom: "1.2rem", animation: "fadeUp 0.8s 0.1s ease both" }}>
            Votre ferme,<br />
            <span className="shimmer-text">entièrement maîtrisée.</span>
          </h1>

          <p style={{ fontSize: "1.05rem", color: "var(--text-muted)", lineHeight: 1.8, maxWidth: 500, marginBottom: "2.5rem", fontWeight: 300, animation: "fadeUp 0.8s 0.2s ease both" }}>
            FermeGest centralise la gestion de vos animaux, productions, stocks et ventes. Conçu pour les éleveurs de Fianarantsoa, pensé pour la réalité du terrain malgache.
          </p>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: "3.5rem", animation: "fadeUp 0.8s 0.3s ease both" }}>
            <button className="btn-primary" onClick={() => setShowLogin(true)} style={{ fontSize: 15, padding: "13px 28px" }}>
              Accéder à mon espace →
            </button>
            <button className="btn-ghost" onClick={() => goTo("modules")}>
              Voir les modules ↓
            </button>
          </div>

          {/* Stats row */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, animation: "fadeUp 0.8s 0.4s ease both" }}>
            {[["🐄","142","Animaux actifs"],["🥛","284 L","Lait / jour"],["🥚","1 240","Œufs / mois"],["🌿","8 ans","Expérience"]].map(([icon, val, label]) => (
              <div key={label} style={{ borderLeft: "1px solid var(--border)", paddingLeft: 14 }}>
                <div style={{ fontSize: 18, marginBottom: 2 }}>{icon}</div>
                <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.5rem", fontWeight: 700, color: "var(--green-200)", lineHeight: 1 }}>{val}</div>
                <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════ TICKER ═══════════════════════════════ */}
      <div style={{ background: "var(--green-700)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)", padding: "14px 0", overflow: "hidden" }}>
        <div style={{ display: "flex", gap: "3rem", whiteSpace: "nowrap", animation: "shimmer 0s" }}>
          {["🐄 Élevage bovin, porcin & volaille","🥛 Production laitière traçable","🌾 Gestion des fourrages et stocks","💊 Suivi santé & rappels vétérinaires","🌿 Agriculture circulaire & engrais","💰 Ventes en Ariary (MGA)","📊 Rapports hebdomadaires & mensuels","🔐 Accès sécurisé par rôle"].map((t, i) => (
            <span key={i} style={{ fontSize: 13, fontWeight: 500, color: "var(--green-200)", display: "inline-flex", alignItems: "center", gap: 8 }}>
              {t}
              <span style={{ color: "var(--green-500)", margin: "0 6px" }}>·</span>
            </span>
          ))}
        </div>
      </div>

      {/* ═══════════════════════════════ MODULES ═══════════════════════════════ */}
      <section id="modules" style={{ padding: "100px 3rem" }}>
        <div ref={addRef} className="reveal" style={{ textAlign: "center", marginBottom: "4rem" }}>
          <span className="section-tag">🗂️ Fonctionnalités</span>
          <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2.2rem, 4vw, 3.2rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "0.8rem" }}>
            8 modules intégrés
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "1rem", maxWidth: 480, margin: "0 auto", fontWeight: 300 }}>
            Chaque aspect de votre exploitation couvert par un module dédié, connecté aux autres en temps réel.
          </p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "1rem", maxWidth: 1100, margin: "0 auto" }}>
          {MODULES.map((m, i) => (
            <div key={i} ref={addRef} className="card-glass reveal" style={{ padding: "1.5rem", transitionDelay: `${i * 0.06}s` }}>
              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "1rem" }}>
                <div style={{ width: 44, height: 44, borderRadius: 12, background: "rgba(151,196,89,0.08)", border: "1px solid var(--border)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22 }}>
                  {m.icon}
                </div>
                <span style={{ fontSize: 11, fontWeight: 600, color: m.color, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)", borderRadius: 100, padding: "3px 10px", letterSpacing: "0.3px" }}>
                  {m.stat}
                </span>
              </div>
              <h3 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.15rem", fontWeight: 700, color: "var(--text-primary)", marginBottom: 8 }}>{m.titre}</h3>
              <p style={{ fontSize: 13, color: "var(--text-muted)", lineHeight: 1.65, fontWeight: 300 }}>{m.desc}</p>
              <div style={{ marginTop: "1.2rem", display: "flex", alignItems: "center", gap: 4, color: m.color, fontSize: 13, fontWeight: 500, cursor: "pointer" }} onClick={() => setShowLogin(true)}>
                Ouvrir le module <span style={{ fontSize: 16 }}>→</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ═══════════════════════════════ À PROPOS ═══════════════════════════════ */}
      <section id="apropos" style={{ padding: "100px 3rem", background: "rgba(0,0,0,0.2)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "5rem", alignItems: "center" }}>
          {/* Left */}
          <div ref={addRef} className="reveal">
            <span className="section-tag">🏡 À propos</span>
            <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2rem, 3.5vw, 3rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "1.2rem", lineHeight: 1.15 }}>
              Une ferme moderne au cœur des <em style={{ color: "var(--green-300)", fontStyle: "italic" }}>Hautes Terres</em>
            </h2>
            <p style={{ color: "var(--text-muted)", fontSize: "0.95rem", lineHeight: 1.85, marginBottom: "1.2rem", fontWeight: 300 }}>
              Fondée à Fianarantsoa, la Ferme Fianarantsoa associe traditions d'élevage malgaches et outils numériques modernes. FermeGest est né du besoin concret de centraliser la gestion d'une exploitation en croissance.
            </p>
            <p style={{ color: "var(--text-muted)", fontSize: "0.95rem", lineHeight: 1.85, marginBottom: "2rem", fontWeight: 300 }}>
              Avec plus de 140 animaux actifs répartis sur 6 enclos spécialisés, la ferme contribue activement à l'économie locale de la région Haute Matsiatra — production laitière, avicole et porcine incluses.
            </p>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: "2rem" }}>
              {[["🏡","6 enclos spécialisés"],["👥","12 employés actifs"],["📱","Gestion 100% numérique"],["🌱","Agriculture circulaire"],["📍","Fianarantsoa, MG"],["🏆","8 ans d'expérience"]].map(([icon, txt]) => (
                <div key={txt} className="security-badge" style={{ borderRadius: 10, padding: "10px 14px" }}>
                  <span style={{ fontSize: 16 }}>{icon}</span>
                  <span style={{ fontSize: 13, color: "var(--text-muted)", fontWeight: 400 }}>{txt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right — team */}
          <div ref={addRef} className="reveal" style={{ transitionDelay: "0.15s" }}>
            <div className="card-glass" style={{ padding: "2rem", marginBottom: "1rem" }}>
              <h3 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.2rem", fontWeight: 700, color: "var(--green-200)", marginBottom: "1.2rem" }}>Notre équipe de direction</h3>
              {TEAM.map((t, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, padding: "12px 0", borderBottom: i < TEAM.length - 1 ? "1px solid var(--border)" : "none" }}>
                  <div style={{ width: 42, height: 42, borderRadius: "50%", background: t.avatar, border: "1px solid var(--border-bright)", display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "'Outfit', sans-serif", fontWeight: 700, fontSize: 14, color: "var(--green-100)", flexShrink: 0 }}>{t.initiales}</div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14, color: "var(--text-primary)" }}>{t.nom}</div>
                    <div style={{ fontSize: 12, color: "var(--text-muted)" }}>{t.role}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Mission card */}
            <div style={{ background: "rgba(99,153,34,0.08)", border: "1px solid rgba(99,153,34,0.2)", borderRadius: 16, padding: "1.5rem" }}>
              <div style={{ fontSize: 22, marginBottom: 8 }}>🎯</div>
              <h4 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.1rem", fontWeight: 700, color: "var(--green-200)", marginBottom: 6 }}>Notre mission</h4>
              <p style={{ fontSize: 13, color: "var(--text-muted)", lineHeight: 1.7, fontWeight: 300 }}>
                Rendre la gestion agricole accessible, traçable et efficace pour chaque éleveur de Madagascar, quelle que soit la taille de son exploitation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════ SÉCURITÉ ═══════════════════════════════ */}
      <section id="securite" style={{ padding: "100px 3rem" }}>
        <div ref={addRef} className="reveal" style={{ textAlign: "center", marginBottom: "4rem" }}>
          <span className="section-tag">🔐 Sécurité</span>
          <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2.2rem, 4vw, 3.2rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "0.8rem" }}>
            Vos données, protégées
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "1rem", maxWidth: 460, margin: "0 auto", fontWeight: 300 }}>
            FermeGest a été conçu avec la sécurité comme fondation, pas comme ajout. Chaque couche est pensée pour protéger l'intégrité de vos données d'exploitation.
          </p>
        </div>

        <div style={{ maxWidth: 1000, margin: "0 auto" }}>
          {/* Big security visual */}
          <div ref={addRef} className="reveal" style={{ textAlign: "center", marginBottom: "3rem" }}>
            <div style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: 100, height: 100, borderRadius: "50%", background: "rgba(99,153,34,0.1)", border: "1px solid rgba(99,153,34,0.25)", fontSize: 44, position: "relative" }}>
              🛡️
              <div style={{ position: "absolute", inset: -8, borderRadius: "50%", border: "1px solid rgba(99,153,34,0.15)", animation: "pulse-ring 2s ease-out infinite" }} />
              <div style={{ position: "absolute", inset: -16, borderRadius: "50%", border: "1px solid rgba(99,153,34,0.08)", animation: "pulse-ring 2s ease-out infinite 0.5s" }} />
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "1rem" }}>
            {SECURITY_ITEMS.map((s, i) => (
              <div key={i} ref={addRef} className="security-badge reveal" style={{ borderRadius: 14, padding: "18px 20px", flexDirection: "column", alignItems: "flex-start", transitionDelay: `${i * 0.07}s` }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
                  <span style={{ fontSize: 22 }}>{s.icon}</span>
                  <span style={{ fontWeight: 600, fontSize: 14, color: "var(--text-primary)" }}>{s.titre}</span>
                </div>
                <p style={{ fontSize: 13, color: "var(--text-muted)", lineHeight: 1.65, fontWeight: 300, margin: 0 }}>{s.desc}</p>
              </div>
            ))}
          </div>

          {/* Compliance banner */}
          <div ref={addRef} className="reveal" style={{ marginTop: "2rem", background: "rgba(99,153,34,0.06)", border: "1px solid rgba(99,153,34,0.15)", borderRadius: 16, padding: "1.5rem 2rem", display: "flex", alignItems: "center", gap: "1.5rem", flexWrap: "wrap" }}>
            <div style={{ fontSize: 28 }}>✅</div>
            <div style={{ flex: 1, minWidth: 200 }}>
              <div style={{ fontWeight: 600, fontSize: 15, color: "var(--green-200)", marginBottom: 4 }}>Conformité & Bonnes pratiques</div>
              <div style={{ fontSize: 13, color: "var(--text-muted)", fontWeight: 300 }}>FermeGest respecte les bonnes pratiques de développement sécurisé Django — authentification robuste, protection CSRF, validation des données côté serveur, accès basé sur les rôles (RBAC).</div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════ FAQ ═══════════════════════════════ */}
      <section id="faq" style={{ padding: "100px 3rem", background: "rgba(0,0,0,0.15)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)" }}>
        <div style={{ maxWidth: 720, margin: "0 auto" }}>
          <div ref={addRef} className="reveal" style={{ textAlign: "center", marginBottom: "3.5rem" }}>
            <span className="section-tag">❓ FAQ</span>
            <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2.2rem, 4vw, 3.2rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "0.8rem" }}>
              Questions fréquentes
            </h2>
            <p style={{ color: "var(--text-muted)", fontSize: "1rem", fontWeight: 300 }}>Les réponses aux questions les plus courantes sur l'utilisation de FermeGest.</p>
          </div>

          {FAQ_ITEMS.map((item, i) => (
            <div key={i} ref={addRef} className="reveal" style={{ borderBottom: "1px solid var(--border)", transitionDelay: `${i * 0.07}s` }}>
              <button className="accordion-btn" onClick={() => setOpenFaq(openFaq === i ? null : i)}>
                <span style={{ fontSize: 15, fontWeight: 500 }}>{item.q}</span>
                <span style={{ color: "var(--green-400)", fontSize: 22, transition: "transform 0.25s", transform: openFaq === i ? "rotate(45deg)" : "none", flexShrink: 0, marginLeft: 12 }}>+</span>
              </button>
              {openFaq === i && (
                <div style={{ paddingBottom: 20, animation: "fadeUp 0.25s ease" }}>
                  <p style={{ fontSize: 14, color: "var(--text-muted)", lineHeight: 1.75, fontWeight: 300 }}>{item.r}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* ═══════════════════════════════ CONFIDENTIALITÉ ═══════════════════════════════ */}
      <section id="confidentialite" style={{ padding: "100px 3rem" }}>
        <div style={{ maxWidth: 860, margin: "0 auto" }}>
          <div ref={addRef} className="reveal" style={{ textAlign: "center", marginBottom: "3.5rem" }}>
            <span className="section-tag">📄 Légal</span>
            <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2.2rem, 4vw, 3.2rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "0.6rem" }}>
              Politique de confidentialité
            </h2>
            <p style={{ color: "var(--text-muted)", fontSize: 13 }}>Dernière mise à jour : Mai 2025 · Ferme Fianarantsoa, Madagascar</p>
          </div>

          {/* Tabs */}
          <div ref={addRef} className="reveal" style={{ display: "flex", gap: 8, flexWrap: "wrap", justifyContent: "center", marginBottom: "2.5rem" }}>
            {[["collecte","📊 Données collectées"],["utilisation","🔧 Utilisation"],["droits","⚖️ Vos droits"]].map(([id, label]) => (
              <button key={id} onClick={() => setActivePrivacy(id)} style={{
                padding: "9px 20px", borderRadius: 100, cursor: "pointer",
                fontFamily: "'Outfit', sans-serif", fontSize: 13, fontWeight: 500,
                border: activePrivacy === id ? "1px solid var(--green-400)" : "1px solid var(--border)",
                background: activePrivacy === id ? "rgba(99,153,34,0.12)" : "transparent",
                color: activePrivacy === id ? "var(--green-300)" : "var(--text-muted)",
                transition: "all 0.2s",
              }}>{label}</button>
            ))}
          </div>

          {/* Content */}
          <div ref={addRef} className="card-glass reveal" style={{ padding: "2.5rem" }}>
            <h3 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.5rem", fontWeight: 700, color: "var(--green-200)", marginBottom: "0.8rem" }}>{pc.titre}</h3>
            <p style={{ fontSize: "0.95rem", color: "var(--text-muted)", lineHeight: 1.85, marginBottom: "1.5rem", fontWeight: 300 }}>{pc.contenu}</p>
            <div style={{ borderTop: "1px solid var(--border)", paddingTop: "1.2rem" }}>
              <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", color: "var(--green-400)", marginBottom: 12 }}>Points clés</div>
              <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: 10 }}>
                {pc.points.map((p, i) => (
                  <li key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
                    <span style={{ color: "var(--green-400)", fontSize: 16, marginTop: 1, flexShrink: 0 }}>✓</span>
                    <span style={{ fontSize: 14, color: "var(--text-muted)", lineHeight: 1.6, fontWeight: 300 }}>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Contact */}
          <div ref={addRef} className="reveal" style={{ marginTop: "1.5rem", background: "rgba(99,153,34,0.06)", border: "1px solid rgba(99,153,34,0.15)", borderRadius: 14, padding: "1.2rem 1.5rem", display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ fontSize: 24 }}>📧</span>
            <div>
              <div style={{ fontSize: 14, fontWeight: 600, color: "var(--green-200)", marginBottom: 2 }}>Pour exercer vos droits</div>
              <div style={{ fontSize: 13, color: "var(--text-muted)", fontWeight: 300 }}>ferme.fianarantsoa@gmail.com · +261 34 XX XXX XX</div>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════ CTA FINAL ═══════════════════════════════ */}
      <section style={{ padding: "100px 3rem", textAlign: "center", background: "linear-gradient(180deg, transparent 0%, rgba(27,52,16,0.4) 100%)", borderTop: "1px solid var(--border)" }}>
        <div ref={addRef} className="reveal">
          <div style={{ fontSize: 48, marginBottom: "1.2rem" }}>🌾</div>
          <h2 style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "clamp(2.4rem, 5vw, 4rem)", fontWeight: 700, color: "var(--text-primary)", marginBottom: "1rem", lineHeight: 1.1 }}>
            Prêt à digitaliser<br /><span className="shimmer-text">votre ferme ?</span>
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "1rem", marginBottom: "2.5rem", fontWeight: 300 }}>
            Rejoignez FermeGest et prenez le contrôle total de votre exploitation dès aujourd'hui.
          </p>
          <button className="btn-primary" onClick={() => setShowLogin(true)} style={{ fontSize: 16, padding: "15px 36px", boxShadow: "0 12px 40px rgba(99,153,34,0.3)" }}>
            🚀 Accéder à FermeGest
          </button>
        </div>
      </section>

      {/* ═══════════════════════════════ FOOTER ═══════════════════════════════ */}
      <footer style={{ background: "var(--green-950)", borderTop: "1px solid var(--border)", padding: "56px 3rem 28px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", gap: "3rem", marginBottom: "3rem" }}>
            {/* Brand */}
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
                <div style={{ fontSize: 24 }}>🌾</div>
                <div style={{ fontFamily: "'Cormorant Garamond', serif", fontSize: "1.2rem", fontWeight: 700, color: "var(--green-200)" }}>FermeGest</div>
              </div>
              <p style={{ fontSize: 13, color: "var(--text-muted)", lineHeight: 1.75, maxWidth: 240, fontWeight: 300 }}>
                Système de gestion agricole intégré pour la Ferme Fianarantsoa, Madagascar. Pensé pour les éleveurs du terrain.
              </p>
            </div>

            {/* Links */}
            {[
              { titre: "Application", liens: ["Tableau de bord","Animaux","Productions","Stocks","Ventes"] },
              { titre: "Ressources", liens: ["Documentation","Guide utilisateur","API REST","Support technique"] },
              { titre: "Légal", liens: ["Confidentialité","Conditions d'utilisation","Mentions légales","Contact"] },
            ].map(({ titre, liens }) => (
              <div key={titre}>
                <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: "1.5px", textTransform: "uppercase", color: "var(--green-400)", marginBottom: 14 }}>{titre}</div>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {liens.map(l => <a key={l} className="footer-link" onClick={() => l === "Confidentialité" && goTo("confidentialite")}>{l}</a>)}
                </div>
              </div>
            ))}
          </div>

          {/* Bottom bar */}
          <div style={{ borderTop: "1px solid var(--border)", paddingTop: 20, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
            <span style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 300 }}>© 2025 FermeGest · Fianarantsoa, Madagascar · Tous droits réservés</span>
            <div style={{ display: "flex", gap: 20 }}>
              {["Confidentialité","CGU","Mentions légales"].map(l => (
                <a key={l} className="footer-link" style={{ fontSize: 12 }}>{l}</a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
