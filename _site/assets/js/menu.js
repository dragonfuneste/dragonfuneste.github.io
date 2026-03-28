document.addEventListener("DOMContentLoaded", function() {
    const footerHTML = `
    <footer class="bottom-menu">
        <a href="index.html" class="menu-box">Main Page</a>
        <a href="about.html" class="menu-box">About Me</a>
        <a href="research.html" class="menu-box">Research</a>
        <a href="projects.html" class="menu-box">Projects</a>
        <a href="contact.html" class="menu-box">Contact</a>
        <a href="repository.html" class="menu-box">Repository</a>
    </footer>`;
    
    // Insère le menu à la fin du body
    document.body.insertAdjacentHTML('beforeend', footerHTML);
});