$(document).ready(function () {
    var tablaEscogerProducto = $('#tablaEscogerProductos').DataTable({
        'lengthMenu': [
            [10, 25, 50, -1],
            [10, 25, 50, 'All']
        ],
        "pageLength": 10,
    });
    var tablaTerceros = $('#tablaEscogerTercero').DataTable({
        'lengthMenu': [
            [10, 25, 50, -1],
            [10, 25, 50, 'All']
        ],
        "pageLength": 10,
    });
    $('table').on('click', 'button[type="button"]', function (e) {
        $(this).closest('tr').remove()
        totalizarCompra()
    })
    $('table').on('change', 'input[type="number"]', function (e) {
        var row = $(this).closest('tr')
        var cantidad = $(row[0].childNodes[3].childNodes[0]).val()
        var costo = $(row[0].childNodes[4].childNodes[0]).val()
        var total = $(row[0].childNodes[5].childNodes[0]).val(cantidad * costo)
        totalizarCompra()
    })
    $('#tablaEscogerProductos tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            tablaEscogerProducto.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        var pos = tablaEscogerProducto.row('.selected').index();
        var row = tablaEscogerProducto.row(pos).data();
        var productoEscogido = row[0]
        tablaEscogerProducto.$('tr.selected').removeClass('selected');
        $('#modalEscogerProducto').modal('hide')
        AgregarProdDetalle(productoEscogido)
    });
    $('#tablaEscogerTercero tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            tablaTerceros.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        var pos = tablaTerceros.row('.selected').index();
        var row = tablaTerceros.row(pos).data();
        var Cedula = row[0]
        var Nombre = row[1]
        $('#proveedorId').val(Cedula)
        $('#nombreProveedor').val(Nombre)
        $('#modalEscogerTercero').modal('hide')
    });

    function AgregarProdDetalle(codigo) {
        $.ajax({
            'type': 'GET',
            'url': '/compras/nuevo',
            'data': {
                'producto': codigo,
            },
            success: function (response) {
                var info_producto = JSON.parse(response['info_producto'])[0]['fields']
                var costo_producto = response['info_costo']
                var descripcion = info_producto['nombre']
                var precio = info_producto['precio']

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
                            .attr('min', '1').val(0)
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
                            .val(0).prop('readonly', true)
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
        })
    }

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
    $('#formNuevoProducto').on('submit', function (e) {
        e.preventDefault();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var formData = new FormData(document.getElementById('formNuevoProducto'));
        formData.append('csrfmiddlewaretoken', csrftoken)
        $.ajax({
            type: 'POST',
            url: '/compras/nuevo',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (response) {
                passed = response['passed']
                codigo = response['codigo']
                descripcion = response['descripcion']
                stock = 0
                precio = response['precio']
                console.log(codigo, descripcion, precio)
                if (passed) {
                    tablaEscogerProducto.row.add([
                        codigo,
                        descripcion,
                        stock,
                        precio
                    ]).draw(false)
                } else {
                    alert('Ocurrio un error al intentar grabar el producto, vuelve a intentar')
                }
                $('#modalNuevoProducto').modal('hide')
                $('#modalEscogerProducto').modal('show')
            }
        }); /* Aqui termina el ajax */

    })
})