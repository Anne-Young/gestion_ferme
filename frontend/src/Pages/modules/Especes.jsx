// src/sousMenu/Espece.jsx

import { useState, useEffect } from "react";

const COLORS = {
  emerald50: "#ecfdf5",
  emerald100: "#d1fae5",
  emerald200: "#a7f3d0",
  emerald300: "#6ee7b7",
  emerald400: "#34d399",
  emerald500: "#10b981",
  emerald600: "#059669",
  emerald700: "#047857",
  emerald800: "#065f46",
  emerald900: "#064e3b",
  blanc: "#FFFFFF",
  rouge: "#dc2626",
  rougeClair: "#fee2e2",
};

export default function Espece() {
  const [items, setItems] = useState([]);

  const [loading, setLoading] = useState(true);

  const [showModal, setShowModal] = useState(false);

  const [modalMode, setModalMode] = useState("create");

  const [selectedItem, setSelectedItem] = useState(null);

  const [formData, setFormData] = useState({
    nom_espece: "",
    description: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const [error, setError] = useState("");

  const [successMessage, setSuccessMessage] = useState("");

  // =========================
  // TOKEN
  // =========================

  const getToken = () => {
    return localStorage.getItem("token");
  };

  // =========================
  // CHARGEMENT INITIAL
  // =========================

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        const response = await fetch(
          "/api/ferme/especes/",
          {
            headers: {
              Authorization: `Bearer ${getToken()}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();

          setItems(data);
        } else {
          console.error(
            "Erreur lors du chargement"
          );
        }
      } catch (err) {
        console.error("Erreur :", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // =========================
  // RELOAD ITEMS
  // =========================

  const reloadItems = async () => {
    try {
      const response = await fetch(
        "/api/ferme/especes/",
        {
          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();

        setItems(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // =========================
  // MESSAGE SUCCÈS
  // =========================

  const showSuccess = (message) => {
    setSuccessMessage(message);

    setTimeout(() => {
      setSuccessMessage("");
    }, 3000);
  };

  // =========================
  // OUVRIR MODAL AJOUT
  // =========================

  const handleAdd = () => {
    setModalMode("create");

    setSelectedItem(null);

    setFormData({
      nom_espece: "",
      description: "",
    });

    setError("");

    setShowModal(true);
  };

  // =========================
  // OUVRIR MODAL MODIF
  // =========================

  const handleEdit = (item) => {
    setModalMode("edit");

    setSelectedItem(item);

    setFormData({
      nom_espece: item.nom_espece,
      description: item.description || "",
    });

    setError("");

    setShowModal(true);
  };

  // =========================
  // OUVRIR MODAL DELETE
  // =========================

  const handleDeleteClick = (item) => {
    setModalMode("delete");

    setSelectedItem(item);

    setError("");

    setShowModal(true);
  };

  // =========================
  // CREATE
  // =========================

  const handleCreate = async () => {
    if (!formData.nom_espece.trim()) {
      setError("Le nom est requis");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(
        "/api/ferme/especes/create/",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",

            Authorization: `Bearer ${getToken()}`,
          },

          body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        setShowModal(false);

        showSuccess(
          "Espèce ajoutée avec succès"
        );

        await reloadItems();
      } else {
        const data = await response.json();

        setError(
          data.error ||
            "Erreur lors de l'ajout"
        );
      }
    } catch (err) {
      console.error(err);

      setError("Erreur de connexion");
    } finally {
      setIsSubmitting(false);
    }
  };

  // =========================
  // UPDATE
  // =========================

  const handleUpdate = async () => {
    if (!selectedItem) return;

    if (!formData.nom_espece.trim()) {
      setError("Le nom est requis");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(
        `/api/ferme/especes/${selectedItem.id}/update/`,
        {
          method: "PUT",

          headers: {
            "Content-Type": "application/json",

            Authorization: `Bearer ${getToken()}`,
          },

          body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        setShowModal(false);

        showSuccess(
          "Espèce modifiée avec succès"
        );

        await reloadItems();
      } else {
        const data = await response.json();

        setError(
          data.error ||
            "Erreur lors de la modification"
        );
      }
    } catch (err) {
      console.error(err);

      setError("Erreur de connexion");
    } finally {
      setIsSubmitting(false);
    }
  };

  // =========================
  // DELETE
  // =========================

  const handleDelete = async () => {
    if (!selectedItem) return;

    setIsSubmitting(true);

    try {
      const response = await fetch(
        `/api/ferme/especes/${selectedItem.id}/delete/`,
        {
          method: "DELETE",

          headers: {
            Authorization: `Bearer ${getToken()}`,
          },
        }
      );

      if (response.ok) {
        setShowModal(false);

        showSuccess(
          "Espèce supprimée avec succès"
        );

        await reloadItems();
      } else {
        const data = await response.json();

        setError(
          data.error ||
            "Erreur lors de la suppression"
        );
      }
    } catch (err) {
      console.error(err);

      setError("Erreur de connexion");
    } finally {
      setIsSubmitting(false);
    }
  };

  // =========================
  // SUBMIT
  // =========================

  const handleSubmit = () => {
    if (modalMode === "create") {
      handleCreate();
    }

    if (modalMode === "edit") {
      handleUpdate();
    }

    if (modalMode === "delete") {
      handleDelete();
    }
  };

  return (
    <div>
      <h2
        style={{
          color: COLORS.emerald700,
        }}
      >
        Gestion des espèces
      </h2>

      <button onClick={handleAdd}>
        + Nouvelle espèce
      </button>

      {successMessage && (
        <p
          style={{
            color: COLORS.emerald700,
          }}
        >
          {successMessage}
        </p>
      )}

      {loading ? (
        <p>Chargement...</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: 20,
          }}
        >
          <thead>
            <tr>
              <th>ID</th>

              <th>Nom</th>

              <th>Description</th>

              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>

                <td>{item.nom_espece}</td>

                <td>
                  {item.description || "—"}
                </td>

                <td>
                  <button
                    onClick={() =>
                      handleEdit(item)
                    }
                  >
                    Modifier
                  </button>

                  <button
                    onClick={() =>
                      handleDeleteClick(item)
                    }
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* MODAL */}

      {showModal && (
        <div style={{ marginTop: 20 }}>
          <h3>
            {modalMode === "create" &&
              "Ajouter"}

            {modalMode === "edit" &&
              "Modifier"}

            {modalMode === "delete" &&
              "Supprimer"}
          </h3>

          {modalMode !== "delete" && (
            <>
              <input
                type="text"
                placeholder="Nom espèce"
                value={formData.nom_espece}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    nom_espece:
                      e.target.value,
                  })
                }
              />

              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    description:
                      e.target.value,
                  })
                }
              />
            </>
          )}

          {modalMode === "delete" && (
            <p>
              Supprimer :
              <strong>
                {" "}
                {
                  selectedItem?.nom_espece
                }
              </strong>
              ?
            </p>
          )}

          {error && (
            <p
              style={{
                color: COLORS.rouge,
              }}
            >
              {error}
            </p>
          )}

          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Chargement..."
              : modalMode === "create"
              ? "Ajouter"
              : modalMode === "edit"
              ? "Modifier"
              : "Supprimer"}
          </button>

          <button
            onClick={() =>
              setShowModal(false)
            }
            disabled={isSubmitting}
          >
            Annuler
          </button>
        </div>
      )}
    </div>
  );
}