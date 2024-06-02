
    // Lista de productos seleccionados
    let productosSeleccionados = [];

    function addProduct(id, nombre, descripcion, stock, precio,) {
        // Comprobar si el producto ya está en la lista
        const existe = productosSeleccionados.find(producto => producto.id === id);
        if (existe) {
            alert('El producto ya está en la lista');
            return;
        }
        
        if (parseInt(stock) === 0) {
            alert('No hay stock disponible para este producto');
            return;
        }

        const producto = {
            id: id,
            nombre: nombre,
            descripcion: descripcion,
            stock: parseInt(stock),
            precio: parseFloat(precio),
            cantidad: 1,
            subtotal: parseFloat(precio)
        };
        productosSeleccionados.push(producto);
        actualizarTabla();
    }

    function removeProduct(id) {
        const productId = id.toString(); // Convertir el ID a una cadena de texto
        productosSeleccionados = productosSeleccionados.filter(producto => producto.id !== productId);
        actualizarTabla();
    }

    function actualizarCantidad(id, cantidadInput) {
        const cantidad = parseInt(cantidadInput.value);
        const producto = productosSeleccionados.find(producto => producto.id === id);

        if (cantidad > producto.stock) {
            alert('La cantidad no puede ser mayor al stock disponible.');
            cantidadInput.value = producto.stock; // Revertir a la cantidad máxima disponible
            producto.cantidad = producto.stock;
        } else {
            producto.cantidad = cantidad;
        }

        producto.subtotal = producto.precio * producto.cantidad;
        actualizarTabla();
    }

    function actualizarTabla() {
        const tbody = document.querySelector('#productosSeleccionados tbody');
        tbody.innerHTML = '';

        productosSeleccionados.forEach(producto => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${producto.id}</td>
                <td>${producto.nombre}</td>
                <td>${producto.descripcion}</td>
                <td>${producto.stock}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td><input type="number" class="form-control" value="${producto.cantidad}" onchange="actualizarCantidad('${producto.id}', this)"></td>
                <td>$${producto.subtotal.toFixed(2)}</td>
                <td><button class="btn btn-danger" onclick="removeProduct('${producto.id}')"><i class="fas fa-trash"></i></button></td>
            `;
            tbody.appendChild(row);
        });
    }

    // Enviar productos seleccionados al servidor
    document.getElementById('miFormulario').addEventListener('submit', function(event) {
        if (productosSeleccionados.length === 0) {
            alert('Debe agregar al menos un producto antes de guardar la solicitud.');
            event.preventDefault();
            return;
        }

        const inputProductos = document.createElement('input');
        inputProductos.type = 'hidden';
        inputProductos.name = 'productos';
        inputProductos.value = JSON.stringify(productosSeleccionados);
        this.appendChild(inputProductos);
    });
