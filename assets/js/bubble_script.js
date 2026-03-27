// Texte des slides
const slideTexts = [
  "Loubet--Bonino Grégory", 
  " ", 
  "Main Question", 
  "Research Topics", 
  "RTI", 
  "SubQuestion RTI",
];

// Récupération de la couleur CSS hex
const rootStyles = getComputedStyle(document.documentElement);
const pinkHex = rootStyles.getPropertyValue('--pink-base').trim(); // "#ff64b4"

// Fonction pour convertir un hex en objet {r,g,b}
function hexToRgb(hex) {
    hex = hex.replace(/^#/, '');
    if(hex.length === 3) hex = hex.split('').map(h => h+h).join('');
    const bigint = parseInt(hex, 16);
    return {
        r: (bigint >> 16) & 255,
        g: (bigint >> 8) & 255,
        b: bigint & 255
    };
}

const pinkBaseRGB = hexToRgb(pinkHex);

// Bulles animées
const bubbleContainer = document.getElementById("bubble-container");

function createBubble() {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  const size = Math.random() * 40 + 10;
  bubble.style.width = bubble.style.height = size + "px";
  bubble.style.left = Math.random() * 100 + "vw";
  const duration = 5 + Math.random() * 5;
  bubble.style.animationDuration = duration + "s";

  const g = pinkBaseRGB.g + Math.random() * 50;
  const b = pinkBaseRGB.b + Math.random() * 50;

  bubble.style.background = `rgba(${pinkBaseRGB.r},${g},${b},0.3)`;
  bubble.style.boxShadow = `0 0 15px rgba(${pinkBaseRGB.r},${g},${b},0.8)`;

  bubbleContainer.appendChild(bubble);
  setTimeout(()=>bubble.remove(), duration*1000);
}

function createFastBubble() {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  const size = Math.random() * 30 + 10;
  bubble.style.width = bubble.style.height = size + "px";
  bubble.style.left = Math.random() * 100 + "vw";
  const duration = 1 + Math.random() * 2;
  bubble.style.animationDuration = duration + "s";

  const g = pinkBaseRGB.g + Math.random() * 50;
  const b = pinkBaseRGB.b + Math.random() * 50;

  bubble.style.background = `rgba(${pinkBaseRGB.r},${g},${b},0.5)`;
  bubble.style.boxShadow = `0 0 20px rgba(${pinkBaseRGB.r},${g},${b},0.9)`;

  bubbleContainer.appendChild(bubble);
  setTimeout(()=>bubble.remove(), duration*1000);
}

setInterval(createBubble, 200);

// Slides
const slides = document.querySelectorAll(".slide-frame");
const totalSlides = slides.length;
let currentSlide = 0;

// Bulles de navigation
const navContainer = document.getElementById("nav-bubbles");
const navBubbles = [];
for(let i=0;i<totalSlides;i++){
  const nav = document.createElement("div");
  nav.classList.add("nav-bubble");
  if(i===0) nav.classList.add("active");
  nav.addEventListener("click",()=>goToSlide(i));
  navContainer.appendChild(nav);
  navBubbles.push(nav);
}

// Numéro de slide
const slideNumber = document.getElementById("slide-number");
const slideBottom = document.getElementById("slide-bottom");

function goToSlide(index){
  if(index<0) index=0;
  if(index>=totalSlides) index=totalSlides-1;

  slides.forEach((s,i)=>{
    s.style.transform = `translateY(${(i - index)*100}vh)`;
  });

  // bulles rapides pour transition
  for(let i=0;i<5;i++) createFastBubble();

  currentSlide = index;
  navBubbles.forEach((b,i)=>b.classList.toggle("active",i===index));
  slideNumber.textContent = `${index+1} / ${totalSlides}`;

  // Mettre à jour le texte du bas
  slideBottom.textContent = slideTexts[index];
}

// Overlay clic
const overlay = document.getElementById("click-overlay");
overlay.addEventListener("click",()=>goToSlide(currentSlide+1));      // clic gauche → avancer
overlay.addEventListener("contextmenu",(e)=>{ 
  e.preventDefault(); 
  goToSlide(currentSlide-1); 
}); // clic droit → reculer

// Clavier
window.addEventListener("keydown",(e)=>{
  if(e.key==="ArrowDown" || e.key===" ") goToSlide(currentSlide+1);
  if(e.key==="ArrowUp") goToSlide(currentSlide-1);
});

// Molette
window.addEventListener("wheel",(e)=>{
  if(e.deltaY>0) goToSlide(currentSlide+1);
  else goToSlide(currentSlide-1);
});

// Initialisation : toutes les slides empilées verticalement
slides.forEach((s,i)=>{
  s.style.transform = `translateY(${i*100}vh)`;
  s.style.transition = "transform 0.7s ease";
});
