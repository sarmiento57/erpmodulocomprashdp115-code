document.addEventListener("DOMContentLoaded", function() {
    document.body.addEventListener("click", function(event) {
        // Manejar clic en "Agregar Proveedor"
        if (event.target.closest('.crearProveedorBtn')) {
            event.preventDefault();
            const button = event.target.closest('.crearProveedorBtn');
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

        // Manejar clic en "Editar Proveedor"
        if (event.target.closest('.editarProveedorBtn')) {
            event.preventDefault();
            const button = event.target.closest('.editarProveedorBtn');
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

        // Manejar clic en "Ver Proveedor"
        if (event.target.closest('.verProveedorBtn')) {
            event.preventDefault();
            const button = event.target.closest('.verProveedorBtn');
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

