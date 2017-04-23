$(document).ready(function(){
    $('.datatable').DataTable({
        language: {
            'search': '',
            'lengthMenu': '_MENU_'
          },
    });
    
    /*
     * default lfrtip
     * l - length changing input control
     * f - filtering input
     * t - The table!
     * i - Table information summary
     * p - pagination control
     * r - processing display element
    */
    $('.datatable-simple').DataTable({
        pagingType: 'simple',
        language: {
          'search': '',
          'lengthMenu': '_MENU_'
        },
        dom: 
        "<'row'<'col-sm-12'f>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-6'l><'col-sm-6'p>>",
    });
    
    $('.datatable-simple .dataTables_filter label').css('float','left');
    $('.dataTables_filter > label input').attr('placeholder','Filter');
    
    $('#id_users').chosen({ width: '100%' });
    $('select').chosen();
    
});
