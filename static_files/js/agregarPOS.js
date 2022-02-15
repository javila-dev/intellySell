$(document).ready(function () {
    var productos = JSON.parse('{{productos|escapejs}}')
    $('#nroTicket').val('{{ticket}}')
    $('#idCliente').val('{{obj_ticket.cliente.pk}}')
    $('#nombreCliente').val('{{obj_ticket.cliente.nombre}}')

    for (producto of productos) {
        var codigo = producto['fields']['producto']
        var cantidad = producto['fields']['cantidad']
        var precio = producto['fields']['valor']
        AgregarProdDetalle(codigo, cantidad, precio)
    }

    function AgregarProdDetalle(codigo, cantidad, precio) {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/infoproductos',
            'data': {
                'producto': codigo,
            },
            success: function (response) {
                var info_producto = JSON.parse(response['infoproducto'])[0]['fields']
                var descripcion = info_producto['nombre']
                agregarLineaProducto(codigo, descripcion, precio, cantidad)
                totalizarTicket();
            }
        })
    }

    function totalizarTicket() {
        var rows = $("#tablaProductosCompra tbody").closest('tbody')
        var cantidadTotal = 0
        var costoTotal = 0
        var filas = $("#tablaProductosCompra tr").length - 1
        for (i = 0; i < filas; i++) {
            var fila = rows[0].childNodes[i]
            cantidad = parseInt($(fila.childNodes[3].childNodes[0]).val())
            costo = parseInt($(fila.childNodes[4].childNodes[0]).val())
            cantidadTotal += cantidad
            costoTotal += cantidad * costo
        }
        $('#totalArticulos').text(cantidadTotal)
        $('#totalTicket').text("$" + new Intl.NumberFormat().format(costoTotal))
        $('#totalCobro').val(costoTotal)
        $('#totalTicketCuenta').val(costoTotal)
    }

    function agregarLineaProducto(codigo, descripcion, precio, cantidad = 1) {
        $('#tablaProductosCompra').append(
            $('<tr>')
            .append(
                $('<td>').append(
                    $('<button>').addClass('btn btn-outline-danger borrar').attr('type', 'button').attr('id', 'eliminilarLinea')
                    .prop('readonly', true).append('<i class="fas fa-minus-circle"></i>').attr('style', 'font-size:small')
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'text').attr('name', 'codigoDetalle').attr('style', 'font-size:small')
                    .val(codigo).prop('readonly', true)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control')
                    .attr('type', 'text').attr('name', 'descripcionDetalle').attr('style', 'font-size:small')
                    .val(descripcion).prop('readonly', true)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'cantidadDetalle').attr('style', 'font-size:small')
                    .attr('min', '1').val(cantidad)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'precioDetalle').attr('min', '1').attr('style', 'font-size:small')
                    .val(precio)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'totalDetalle').attr('min', '1').attr('style', 'font-size:small')
                    .val(precio * cantidad).prop('readonly', true)
                )
            )
        )

    }

})