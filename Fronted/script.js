function obtenerNombrePagina(ruta) {
    return decodeURIComponent((ruta || "index.html").split("/").pop() || "index.html").toLowerCase();
}

function normalizarEnlace(href) {
    return (href || "").split("#")[0].split("?")[0].replace(/^\.\//, "").toLowerCase();
}

const paginaActual = obtenerNombrePagina(window.location.pathname);
const enlacesNav = document.querySelectorAll(".navbar .nav-link");

enlacesNav.forEach(function(enlace) {
    const destino = normalizarEnlace(enlace.getAttribute("href"));

    if (destino === paginaActual || (paginaActual === "index.html" && destino === "")) {
        enlace.classList.add("active");
        enlace.setAttribute("aria-current", "page");
    } else {
        enlace.classList.remove("active");
        enlace.removeAttribute("aria-current");
    }
});

// GLightbox: configura la galería para abrir las imágenes en modal.
if (window.GLightbox) {
    GLightbox({
        selector: ".galeria-lightbox",
        touchNavigation: true,
        loop: true,
        autoplayVideos: false
    });
}

// EmailJS: inicializa y maneja el envío del formulario de contacto.
const formularioContacto = document.querySelector("#formulario-contacto");
const mensajeContacto = document.querySelector("#mensaje-contacto");

if (window.emailjs && typeof emailjs.init === "function") {
    emailjs.init({ publicKey: "8pVxMZdI8eYuGyOBz" });
}

if (formularioContacto && window.emailjs) {
    formularioContacto.addEventListener("submit", function(event) {
        event.preventDefault();

        const botonEnviar = formularioContacto.querySelector("button[type='submit']");
        botonEnviar.disabled = true;
        botonEnviar.textContent = "Enviando...";

        emailjs.sendForm("service_miomio", "template_fmfdwyt", formularioContacto)
            .then(function() {
                mensajeContacto.className = "alert alert-success mb-3";
                mensajeContacto.textContent = "Mensaje enviado correctamente.";
                formularioContacto.reset();
            })
            .catch(function(error) {
                console.error("Error de EmailJS:", error);
                mensajeContacto.className = "alert alert-danger mb-3";
                mensajeContacto.textContent = "No se pudo enviar el mensaje. Error: " + (error.text || error.message || error.status || "revisa la configuracion de EmailJS");
            })
            .finally(function() {
                botonEnviar.disabled = false;
                botonEnviar.textContent = "Enviar mensaje";
            });
    });
}

// ========== SCRIPT 1: Botón volver arriba (Back to Top) ==========
// Crea un botón flotante que vuelve al inicio de la página
const crearBotonRetorno = () => {
    const botonRetorno = document.createElement("button");
    botonRetorno.id = "boton-retorno-arriba";
    botonRetorno.innerHTML = "↑";
    botonRetorno.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        border: none;
        border-radius: 50%;
        color: white;
        font-size: 24px;
        cursor: pointer;
        display: none;
        z-index: 999;
        opacity: 0.8;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    `;
    document.body.appendChild(botonRetorno);

    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            botonRetorno.style.display = "block";
        } else {
            botonRetorno.style.display = "none";
        }
    });

    botonRetorno.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    botonRetorno.addEventListener("mouseover", () => {
        botonRetorno.style.opacity = "1";
        botonRetorno.style.transform = "scale(1.1)";
    });

    botonRetorno.addEventListener("mouseout", () => {
        botonRetorno.style.opacity = "0.8";
        botonRetorno.style.transform = "scale(1)";
    });
};
crearBotonRetorno();

// ========== SCRIPT 2: Smooth Scroll mejorado ==========
// Suaviza todos los scrolls y enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(enlace => {
    enlace.addEventListener("click", function(e) {
        const href = this.getAttribute("href");
        if (href !== "#") {
            e.preventDefault();
            const elemento = document.querySelector(href);
            if (elemento) {
                elemento.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }
    });
});

// ========== SCRIPT 3: Animaciones AOS (Animate On Scroll) ==========
// Agrega animaciones cuando los elementos entran en la vista
const observador = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observador.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll(".card, .contenido-card, section").forEach(elemento => {
    elemento.classList.add("elemento-animado");
    observador.observe(elemento);
});

// Esto agrega estilos de animación!
const style = document.createElement("style");
style.textContent = `
    .elemento-animado {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .elemento-animado.visible {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(style);

// ========== SCRIPT 4: Indicador de progreso de lectura ==========
// Muestra una barra que indica cuánto de la página has visto
const crearIndicadorProgreso = () => {
    const barra = document.createElement("div");
    barra.id = "barra-progreso";
    barra.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff9900 0%, #ffbf00 100%);
        width: 0%;
        z-index: 1000;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(barra);

    window.addEventListener("scroll", () => {
        const altura = document.documentElement.scrollHeight - window.innerHeight;
        const progreso = altura > 0 ? (window.scrollY / altura) * 100 : 0;
        barra.style.width = progreso + "%";
    });
};
crearIndicadorProgreso();
