function filterProjects(category, event) {
    // Mise à jour des boutons de filtrage
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if (event) event.target.classList.add('active');

    // Filtrage des cartes
    document.querySelectorAll('.project-card').forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.style.display = "flex";
        } else {
            card.style.display = "none";
        }
    });
}

// Fonction principale pour ouvrir la modale avec gestion média
function openModal(name, desc, skills, context, imagesStr, videosStr) {
    const modal = document.getElementById("projectModal");
    const body = document.getElementById("modalBody");
    
    // Traitement des chaînes de caractères en tableaux
    const images = imagesStr ? imagesStr.split(',').filter(img => img.length > 5) : [];
    const videos = videosStr ? videosStr.split(',').filter(vid => vid.length > 5) : [];

    // Construction du HTML de la modale
    body.innerHTML = `
        <div class="modal-header-block">
            <h2 class="modal-title">${name}</h2>
            <div class="modal-meta">
                ${context ? `<p><strong>Context:</strong> ${context}</p>` : ''}
                ${skills ? `<p class="modal-skills"><strong>Skills:</strong> ${skills}</p>` : ''}
            </div>
        </div>
        
        <div class="modal-description">${desc}</div>
        
        <div class="modal-media-gallery">
            
            ${videos.map(vid => `
                <div class="media-item video-item">
                    <video controls preload="metadata">
                        <source src="${vid}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            `).join('')}

            ${images.map(img => `
                <div class="media-item image-item">
                    <img src="${img}" alt="${name}">
                </div>
            `).join('')}
            
        </div>
    `;

    modal.style.display = "block";
    document.body.style.overflow = "hidden"; // Bloque le scroll du body
}

function closeModal() {
    // Stop toutes les vidéos en cours de lecture lors de la fermeture
    const videos = document.querySelectorAll('#modalBody video');
    videos.forEach(video => video.pause());

    document.getElementById("projectModal").style.display = "none";
    document.body.style.overflow = "auto"; // Réactive le scroll du body
}

// Fermeture en cliquant en dehors de la modale
window.onclick = function(event) {
    const modal = document.getElementById("projectModal");
    if (event.target == modal) {
        closeModal();
    }
}