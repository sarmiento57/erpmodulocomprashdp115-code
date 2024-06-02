document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('formulario');
    var inputs = form.querySelectorAll('input[name^="cantidad_recibida_"], input[name^="subtotal_"], input[name^="impuesto_"], input, select');

    function calcularTotal(fila) {
        var cantidadRecibida = parseInt(fila.querySelector('input[name^="cantidad_recibida_"]').value);
        var precio = parseFloat(fila.querySelector('td:nth-child(5)').textContent.replace('$', ''));
        var impuesto = parseFloat(fila.querySelector('input[name^="impuesto_"]').value);
        var totalImpuesto = (precio * cantidadRecibida) * (impuesto / 100);
        var total = (precio * cantidadRecibida) + totalImpuesto;
        fila.querySelector('input[name^="total_"]').value = total.toFixed(2);
        return totalImpuesto;
    }

    function verificarCantidades() {
        var filas = document.querySelectorAll('tbody tr');
        var cantidadesNoCoinciden = false;

        filas.forEach(function(fila) {
            var cantidad = parseInt(fila.querySelector('td:nth-child(4)').textContent);
            var cantidadRecibida = parseInt(fila.querySelector('input[name^="cantidad_recibida_"]').value);
            if (cantidadRecibida !== cantidad) {
                cantidadesNoCoinciden = true;
            }
        });

        return cantidadesNoCoinciden;
    }

    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (input.hasAttribute('required') && !input.value.trim()) {
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
            if (input.tagName === 'INPUT' || input.tagName === 'SELECT') {
                var fila = input.closest('tr');
                if (fila) {
                    calcularTotal(fila);
                }
            }
        });
    });

    form.addEventListener('submit', function(event) {
        var isValid = true;

        // Verificar campos obligatorios
        inputs.forEach(function(input) {
            if (input.hasAttribute('required') && !input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            // Si hay campos obligatorios vacíos, evitar el envío del formulario y salir de la función
            event.preventDefault();
            event.stopPropagation();
            return;
        }

        // Si todos los campos obligatorios están llenos, verificar cantidades y mostrar mensaje de confirmación si es necesario
        if (verificarCantidades()) {
            if (!confirm("¿Estás seguro de querer confirmar el pago? La cantidad recibida es distinta de la cantidad solicitada para algún producto.")) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
        }
        
        // Si todo está correcto, permitir el envío del formulario
        form.classList.add('was-validated');
    });
});


document.addEventListener("DOMContentLoaded", function() {
    var formulario = document.getElementById("formulario");
    formulario.addEventListener("submit", function() {
        var camposDeshabilitados = document.querySelectorAll("input[disabled], select[disabled], textarea[disabled]");
        for (var i = 0; i < camposDeshabilitados.length; i++) {
            camposDeshabilitados[i].disabled = false;
        }
    });
});