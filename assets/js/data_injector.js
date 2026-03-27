document.addEventListener("DOMContentLoaded", function() {
    console.log("Tentative d'injection des données...");

    if (typeof CV_DATA === 'undefined') {
        console.error("Erreur : CV_DATA n'est pas défini. Vérifie l'import de profile-data.js");
        return;
    }

    const p = CV_DATA.profile;

    // Injection du nom
    const nameEl = document.getElementById('user-name');
    if (nameEl) nameEl.textContent = p.name;

    // Injection du titre
    const titleEl = document.getElementById('user-title');
    if (titleEl) titleEl.textContent = p.title;

    // Injection de la photo
    const photoEl = document.getElementById('user-photo');
    if (photoEl) photoEl.src = p.photo;

    console.log("Injection réussie pour :", p.name);
});