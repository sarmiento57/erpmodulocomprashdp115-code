document.addEventListener("DOMContentLoaded", function() {
    document.body.addEventListener("click", function(event) {
        // Manejar clic en "Crear Producto"
        if (event.target.closest('.crearProductoBtn')) {
            event.preventDefault();
            const button = event.target.closest('.crearProductoBtn');
            const url = button.getAttribute("data-url");

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const modalContent = document.createElement("div");
                    modalContent.innerHTML = html;
                    document.body.appendChild(modalContent);

                    const modal = new bootstrap.Modal(modalContent.querySelector('.modal'));
                    modal.show();
                })
                .catch(error => console.error("Error al cargar el formulario:", error));
        }

        // Manejar clic en "Editar Producto"
        if (event.target.closest('.editarProductoBtn')) {
            event.preventDefault();
            const button = event.target.closest('.editarProductoBtn');
            const url = button.getAttribute("data-url");

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const modalContent = document.createElement("div");
                    modalContent.innerHTML = html;
                    document.body.appendChild(modalContent);

                    const modal = new bootstrap.Modal(modalContent.querySelector('.modal'));
                    modal.show();
                })
                .catch(error => console.error("Error al cargar el formulario:", error));
        }

        // Manejar clic en "Ver Producto"
        if (event.target.closest('.verProductoBtn')) {
            event.preventDefault();
            const button = event.target.closest('.verProductoBtn');
            const url = button.getAttribute("data-url");

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    const modalContent = document.createElement("div");
                    modalContent.innerHTML = html;
                    document.body.appendChild(modalContent);

                    const modal = new bootstrap.Modal(modalContent.querySelector('.modal'));
                    modal.show();
                })
                .catch(error => console.error("Error al cargar el formulario:", error));
        }
    });
});
