document.addEventListener('DOMContentLoaded', function() {
    var diarioSelect = document.getElementById('id_diario');
    var metodoPagoSelect = document.getElementById('id_metodo_pago');
    var cuentaBancariaDiv = document.getElementById('cuenta-bancaria-div');
    var cuentaBancariaInput = document.getElementById('id_cuenta_bancaria');

    function actualizarMetodoPago() {
        if (diarioSelect.value === 'Banco') {
            cuentaBancariaDiv.classList.add('required');
            cuentaBancariaInput.setAttribute('required', 'true');
            cuentaBancariaInput.removeAttribute('disabled');
            metodoPagoSelect.value = 'Transferencia';
            metodoPagoSelect.setAttribute('disabled', 'true');
        } else if (diarioSelect.value === 'Efectivo') {
            cuentaBancariaDiv.classList.remove('required');
            cuentaBancariaInput.removeAttribute('required');
            cuentaBancariaInput.setAttribute('disabled', 'true');
            metodoPagoSelect.value = 'Manual';
            metodoPagoSelect.setAttribute('disabled', 'true');
        } else {
            cuentaBancariaDiv.classList.remove('required');
            cuentaBancariaInput.removeAttribute('required');
            cuentaBancariaInput.removeAttribute('disabled');
            metodoPagoSelect.removeAttribute('disabled');
        }
    }

    diarioSelect.addEventListener('change', actualizarMetodoPago);

    var formulario = document.getElementById('formulario');
    formulario.addEventListener('submit', function(event) {
        if (diarioSelect.value === 'Banco' && cuentaBancariaInput.value.trim() === '') {
            event.preventDefault();
            alert('Por favor, ingresa la cuenta bancaria.');
        }
    });

    actualizarMetodoPago(); 
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