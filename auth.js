// js/auth.js
console.log("auth.js: Script cargado.");

/**
 * Credenciales de los perfiles.
 * Las CLAVES son las contraseñas que el usuario ingresará.
 * Los VALORES son los identificadores de perfil ('1005', '1006').
 */
const PROFILE_CREDENTIALS = {
    "Dmitry": "1005", // Contraseña para el perfil con ID "1005"
    "Miriam": "1006"  // Contraseña para el perfil con ID "1006"
    // Puedes agregar más contraseñas y perfiles aquí:
    // "otraClave": "otroPerfilID",
};
console.log("auth.js: PROFILE_CREDENTIALS definido:", PROFILE_CREDENTIALS);

/**
 * Verifica si el usuario está autenticado y protege la página si no lo está.
 * Esta función se llama en cada página.
 * @returns {boolean} True si el usuario está autenticado y puede continuar, False si el acceso es denegado.
 */
function checkAuthAndProtect() {
    console.log("auth.js: checkAuthAndProtect() iniciado.");
    const isAuthenticated = sessionStorage.getItem('isAuthenticated');
    const currentProfile = sessionStorage.getItem('selectedProfile');
    // Determina si la página actual es index.html
    const isIndexPage = window.location.pathname.endsWith('/') || window.location.pathname.endsWith('index.html') || window.location.pathname.split('/').pop() === '';


    console.log("auth.js: Estado actual - isAuthenticated:", isAuthenticated, "selectedProfile:", currentProfile, "isIndexPage:", isIndexPage);

    if (isAuthenticated === 'true' && currentProfile) {
        console.log("auth.js: Usuario autenticado con perfil. Acceso permitido.");
        // Si estamos en index.html y está autenticado, el script de index.html se encarga de mostrar el contenido.
        return true; // Autenticado, continuar cargando la página
    }

    // No autenticado o falta el perfil
    sessionStorage.removeItem('isAuthenticated');
    sessionStorage.removeItem('selectedProfile');
    console.log("auth.js: No autenticado o sin perfil. Limpiando sessionStorage.");

    if (isIndexPage) {
        // En index.html, no reemplazamos el body. El script de index.html manejará la visualización del login.
        console.log("auth.js: En index.html y no autenticado. El script de index.html mostrará el login.");
        return true; // Permitir que index.html cargue y maneje el login.
    } else {
        // En otras páginas, si no está autenticado, bloquear acceso y mostrar mensaje.
        console.log("auth.js: No en index.html y no autenticado. Bloqueando acceso.");
        document.body.innerHTML = `
            <div style="font-family: 'Inter', sans-serif; text-align:center; padding: 20px; color: #333; background-color: #f8f9fa; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin:0;">
                <style>
                    body { margin: 0; } /* Asegurar que no haya márgenes en el body al reemplazar */
                    .auth-message-container { max-width: 90%; width: 400px; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
                    .auth-title { font-size: 1.6rem; color: #dc3545; margin-bottom: 15px; }
                    .auth-text { font-size: 0.95rem; margin-bottom: 20px; }
                    .auth-button { display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; font-size: 0.95rem; transition: background-color 0.3s; }
                    .auth-button:hover { background-color: #0056b3; }
                    /* Cargar Bootstrap Icons si no están ya (para el ícono) */
                    @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");
                </style>
                <div class="auth-message-container">
                    <h1 class="auth-title"><i class="bi bi-exclamation-triangle-fill" style="font-size: 1.8rem;"></i> Acceso Denegado</h1>
                    <p class="auth-text">Necesitas iniciar sesión para ver esta página. Por favor, regresa a la página principal e ingresa tu clave.</p>
                    <a href="index.html" class="auth-button">Ir a Inicio de Sesión</a>
                </div>
            </div>`;
        return false; // Bloquear carga del contenido original de la página
    }
}

/**
 * Cierra la sesión del usuario.
 */
function logout() {
    console.log("auth.js: logout() llamado.");
    sessionStorage.removeItem('isAuthenticated');
    sessionStorage.removeItem('selectedProfile');
    console.log("auth.js: sessionStorage limpiado para logout.");
    // No usar alert, la redirección es suficiente y más limpia.
    window.location.href = 'index.html'; // Redirige a la página principal (donde se pedirá clave)
}

// Nota: checkAuthAndProtect() se llamará explícitamente desde el script de cada página
// dentro del DOMContentLoaded para asegurar que el DOM esté listo.
console.log("auth.js: Script finalizado. Funciones definidas.");
