

    // Variable para almacenar los productos seleccionados
    let productosSeleccionados = [];

    // Función para actualizar la tabla de productos seleccionados
    function actualizarTabla() {
        const tableBody = document.getElementById('productosSeleccionados').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = '';

        productosSeleccionados.forEach((producto, index) => {
            const row = tableBody.insertRow();
            row.insertCell(0).textContent = producto.id;
            row.insertCell(1).textContent = producto.nombre;
            row.insertCell(2).textContent = producto.descripcion;
            row.insertCell(3).textContent = producto.stock;
            row.insertCell(4).textContent = producto.precio;
            const cantidadCell = row.insertCell(5);
            const cantidadInput = document.createElement('input');
            cantidadInput.type = 'number';
            cantidadInput.value = producto.cantidad;
            cantidadInput.min = '1';
            cantidadInput.addEventListener('change', function() {
                const nuevaCantidad = parseInt(this.value);
                const stockDisponible = producto.stock;
                if (nuevaCantidad <= stockDisponible) {
                    producto.cantidad = nuevaCantidad;
                    producto.subtotal = producto.precio * nuevaCantidad;
                } else {
                    alert('No hay suficiente stock disponible');
                    this.value = producto.cantidad;
                }
                actualizarTabla();
            });
            cantidadCell.appendChild(cantidadInput);
            row.insertCell(6).textContent = producto.subtotal.toFixed(2);
            const actionsCell = row.insertCell(7);
            const deleteButton = document.createElement('button');
            deleteButton.className = 'btn btn-danger';
            deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
            deleteButton.onclick = () => {
                productosSeleccionados.splice(index, 1);
                actualizarTabla();
            };
            actionsCell.appendChild(deleteButton);
        });
    }

    // Función para agregar un producto a los productos seleccionados
   // Función para agregar un producto a los productos seleccionados
function addProduct(id, nombre, descripcion, stock, precio) {
    const cantidad = 1;

    // Verificar si el producto ya está en la lista de productos seleccionados
    const productoExistenteIndex = productosSeleccionados.findIndex(producto => producto.id === parseInt(id));
    if (productoExistenteIndex !== -1) {
        // Si el producto ya existe, agregar uno nuevo encima con los mismos datos
        productosSeleccionados.splice(productoExistenteIndex, 0, productosSeleccionados[productoExistenteIndex]);
    }

    const producto = {
        id: parseInt(id),
        nombre: nombre,
        descripcion: descripcion,
        stock: parseInt(stock),
        precio: parseFloat(precio),
        cantidad: cantidad,
        subtotal: parseFloat(precio) * cantidad
    };

    productosSeleccionados.push(producto);
    actualizarTabla();

    $('#MaterialesModal').modal('hide');
}


    // Inicializar la tabla de productos seleccionados
    window.addEventListener('DOMContentLoaded', (event) => {
        productosSeleccionados = JSON.parse('{{ productos_seleccionados|escapejs }}');
        actualizarTabla();
    });
