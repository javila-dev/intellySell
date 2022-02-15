    $(document).ready(function () {
        var tablaEscogerProducto = $('#tablaEscogerProductos').DataTable({
            'lengthMenu': [
                [10, 25, 50, -1],
                [10, 25, 50, 'All']
            ],
            "pageLength": 10,
            "order": [
                [1, "asc"]
            ]
        });
        var tablaTerceros = $('#tablaEscogerTercero').DataTable({
            'lengthMenu': [
                [10, 25, 50, -1],
                [10, 25, 50, 'All']
            ],
            "pageLength": 10,
            "order": [
                [1, "asc"]
            ]
        });
        var tablaTicketsPdtes = $('#tablaTicketsPdtes').DataTable({
            'lengthMenu': [
                [10, 25, 50, -1],
                [10, 25, 50, 'Todos']
            ],
            "pageLength": 10,
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
            var cantidad = row[2]
            tablaEscogerProducto.$('tr.selected').removeClass('selected');
            $('#modalEscogerProducto').modal('hide')
            if (cantidad < 1) {
                $('#modalAlerta').modal('show')
                $('#tituloAlertaPopUp').text('Advertencia')
                $('#mensajeAlertaPopUp').text('Estas agregando un producto que no tiene existencias')
            }
            AgregarProdDetalle(productoEscogido,1,0)
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
            $('#idCliente').val(Cedula)
            $('#nombreCliente').val(Nombre)
            $('#modalEscogerTercero').modal('hide')
        });
        $('#tablaTicketsPdtes tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                tablaTicketsPdtes.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
            var pos = tablaTicketsPdtes.row('.selected').index();
            var row = tablaTicketsPdtes.row(pos).data();
            var nro_ticket = row[0]
            var Nombre = row[2]
            $('#modalTicketsPdtes').modal('hide')
            recuperarTicket(nro_ticket)
            $('#nombreCliente').val(Nombre)

        });
        $('table').on('click', 'button[type="button"]', function (e) {
            $(this).closest('tr').remove()
            totalizarTicket()
        });
        $('table').on('change', 'input[type="number"]', function (e) {
            var row = $(this).closest('tr')
            var cantidad = $(row[0].childNodes[3].childNodes[0]).val()
            var costo = $(row[0].childNodes[4].childNodes[0]).val()
            var total = $(row[0].childNodes[5].childNodes[0]).val(cantidad * costo)
            totalizarTicket()
        })
        
        $(this).on('submit',function(){
            $('#modalCobrarTicket').modal('hide')
            $('#modalCargando').modal('show')
        })
        function AgregarProdDetalle(codigo,cantidad,precio) {
            $.ajax({
                'type': 'GET',
                'url': '/ajax/infoproductos',
                'data': {
                    'producto': codigo,
                },
                success: function (response) {
                    var info_producto = JSON.parse(response['infoproducto'])[0]['fields']
                    var descripcion = info_producto['nombre']
                    if(precio==0){
                        precio = info_producto['precio']
                    }
                    agregarLineaProducto(codigo, descripcion, precio, cantidad)
                    totalizarTicket()
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
        function recuperarTicket(nroTicket) {
            $.ajax({
                'type': 'GET',
                'url': '/ajax/infoticket',
                'data': {
                    'ticket': nroTicket,
                },
                success: function (response) {
                    $('#tablaProductosCompra tbody tr').remove()
                    var detalle_ticket = JSON.parse(response['productos_ticket'])
                    var info_ticket = JSON.parse(response['info_ticket'])[0]['fields']
                    for (i = 0; i < detalle_ticket.length; i++) {
                        var codigo = detalle_ticket[i]['fields']['producto']
                        var cantidad = detalle_ticket[i]['fields']['cantidad']
                        var precio = detalle_ticket[i]['fields']['valor']
                        AgregarProdDetalle(codigo,cantidad,precio)
                        if (i == detalle_ticket.length - 1) {
                        }
                    }
                    $('#idCliente').val(info_ticket['cliente'])
                    $('#nroTicket').val(nroTicket)
                }
            })
        }
    });
    function Cobrar() {
        var numerofilas = $('#tablaProductosCompra tr').length;
        if (numerofilas < 2) {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('No se puede cobrar un ticket sin lineas')
        } else {
            $('#modalCobrarTicket').modal('show')
        }
    }
    function dejarPendiente() {
        var cliente = $('#idCliente').val()
        var numerofilas = $('#tablaProductosCompra tr').length;
        if (numerofilas < 2) {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('No se puede cobrar un ticket sin lineas')
            return
        }
        if (cliente == '') {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('Para dejar un ticket pendiente debes asignar un cliente primero')
        } else {
            $('#mensajeConfirmacionPopUp').text('¿Estas seguro que deseas dejar este ticket pendiente?')
            $('#btnConfirmar').attr('name', 'btnDejarPendiente')
            $('#modalConfirmar').modal('show')
        }
    }
    function enviarCuenta() {
        var cliente = $('#idCliente').val()
        var numerofilas = $('#tablaProductosCompra tr').length;
        if (numerofilas < 2) {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('No se puede cobrar un ticket sin lineas')
            return
        }
        if (cliente == '') {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('Para dejar un ticket pendiente debes asignar un cliente primero')
        } else {
            $('#modalEnviarCta').modal('show')

        }
    }
    function anularTicket() {
        var nroticket = $('#nroTicket').val()
        if (nroticket != "0000000") {
            $('#modalAnularTicket').modal('show')
        } else {
            $('#modalAlerta').modal('show')
            $('#tituloAlertaPopUp').text('Error')
            $('#mensajeAlertaPopUp').text('La opcion de anular no esta disponible para tickets nuevos')
        }
    }