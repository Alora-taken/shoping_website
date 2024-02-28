console.log("customadmin");
(function($){
    $(document).ready(function(){
        $('#result_list tbody tr').each(function(){
            console.log("customadmin");
            if ($(this).find('td.field-is_deleted_colored').text().trim().toLowerCase() === 'true'){
                $(this).css('background-color', 'red');
            }
        });
    });
})(django.jQuery);
