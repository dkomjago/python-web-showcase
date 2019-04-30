// Restricts input for each element in the set of matched elements to the given inputFilter.
$(document).ready(function() {
    (function ($) {
        $.fn.inputFilter = function (inputFilter) {
            return this.on("input keydown keyup mousedown mouseup select contextmenu drop change", function () {
                if (inputFilter(this.value)) {
                    this.oldValue = this.value;
                    this.oldSelectionStart = this.selectionStart;
                    this.oldSelectionEnd = this.selectionEnd;
                } else if (this.hasOwnProperty("oldValue")) {
                    this.value = this.oldValue;
                    this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
                }
            });
        };
    }(jQuery));

// Restrict input to digits by using a regular expression filter.
    $("#page-input").inputFilter(function (value) {
        return /^\d*$/.test(value) && (value === "" || parseInt(value)>=1)
    });
});

$(document).ready( function(){
    $('#search').keyup(function(){
        $('#page-input').val(1);
        search();
    });
    $('#page-input').keyup(function(){
        if(this.value!=='')search();
    });
    function search(){
        const query = $('#search').val();
        const queryBy = $('#search-by').val();
        const orderBy = $('#order-by').val();
        const perPage = $('#per-page').val();
        const page = $('#page-input').val() - 1;
        $.ajax({
            type: "GET",
            url: '/find',
            data:{
                get_by: queryBy,
                val: query,
                page: page,
                limit: perPage,
                order_by: orderBy,
            },
            success: function(data){
                console.log("SUCCESS");
                console.log(data);
                $('ul').empty();
                if($('#page-input').val()>=data['page_count']) {
                    $('#next').attr({"disabled": true, 'class': 'btn btn-light btn-sm'});
                }
                else{
                    $('#next').attr({"disabled": false, 'class': 'btn btn-primary btn-sm'});
                }
                if($('#page-input').val()==1){
                    $('#previous').attr({"disabled": true, 'class': 'btn btn-light btn-sm'});
                }
                else{
                    $('#previous').attr({"disabled": false, 'class': 'btn btn-primary btn-sm'});
                }
                $.each( data['posts'], function(key,value) {
                    $('#list-posts').append('<li class="list-group-item">'+value+'</li>')
                })
                if(jQuery.isEmptyObject(data['posts']))
                    $('#list-posts').append('<li class="list-group-item">No Results</li>');
            },
            failure: function(data){
                console.log("FAIL");
                console.log(data);
            },
        });
    }
    function changePage(value){
        $("#page-input").val(parseInt($("#page-input").val())+value);
        if($("#page-input").val()<1 || isNaN($("#page-input").val()))
            $("#page-input").val(1);
        search();
    }
    $("#previous").click(function() {changePage(-1)});
    $("#next").click(function() {changePage(1)});
    $("#apply-filters").click(function() {search()});
    search();
});