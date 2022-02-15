$(document).ready(function () {
    $('#proveedorId').val('{{proveedor.pk}}')
    $('#id_nroFactura').val('{{factura}}')
    $('#nombreProveedor').val('{{proveedor.nombre}}')
    var fecha = new Date('{{datos_compra.fecha|date:"c"}}')
    fecha = moment(fecha).add(1, 'days')
    $('#id_Fecha_Factura').datetimepicker('date', fecha)
    var info_producto = JSON.parse('{{detalle_compra|escapejs}}')
    for (i = 0; i < info_producto['len']; i++) {
        var codigo = info_producto[i]['producto']
        var descripcion = info_producto[i]['descripcion']
        var cantidad = info_producto[i]['cantidad']
        var costo_producto = info_producto[i]['costo']
        var costoTotal = info_producto[i]['total']
        var precio = info_producto[i]['precio']
        $('#tablaProductosCompra').append(
            $('<tr>')
            .append(
                $('<td>').append(
                    $('<button>').addClass('btn btn-outline-danger borrar').attr('type', 'button').attr('id', 'eliminilarLinea')
                    .prop('readonly', true).append('<i class="fas fa-minus-circle"></i>')
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center').attr('type', 'text').attr('name', 'codigoDetalle').val(codigo).prop('readonly', true)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control')
                    .attr('type', 'text').attr('name', 'descripcionDetalle')
                    .val(descripcion).prop('readonly', true)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'cantidadDetalle')
                    .attr('min', '1').val(cantidad)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'costoDetalle').attr('min', '1')
                    .val(costo_producto)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'totalDetalle').attr('min', '1')
                    .val(costoTotal).prop('readonly', true)
                )
            )
            .append(
                $('<td>').append(
                    $('<input>').addClass('form-control text-center')
                    .attr('type', 'number').attr('name', 'nuevoPVPDetalle').attr('min', '1')
                    .val(precio)
                )
            )
        )

    }
    totalizarCompra();

    function totalizarCompra() {
        var rows = $("#tablaProductosCompra tbody").closest('tbody')
        var cantidadTotal = 0
        var costoTotal = 0
        var filas = $("#tablaProductosCompra tr").length - 2
        for (i = 0; i < filas; i++) {
            var fila = rows[0].childNodes[i]
            cantidad = parseInt($(fila.childNodes[3].childNodes[0]).val())
            costo = parseInt($(fila.childNodes[4].childNodes[0]).val())
            cantidadTotal += cantidad
            costoTotal += cantidad * costo
        }
        $('#totalCantidad').text(cantidadTotal)
        $('#totalTotal').text("$" + new Intl.NumberFormat().format(costoTotal))
    }

})