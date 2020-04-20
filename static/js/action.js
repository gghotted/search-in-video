$(function(){
    // 검색어 매치 추천
    $('#find_text').autocomplete({
        source: function(request, response){
            $.ajax({
                method: 'get',
                url: '/search/words',
                dataType: 'json',
                data: {find_text: $('#find_text').val()},
                success: function(json_response){
                    var words = json_response.words_list;
                    response(words);
                }
            });
        },
        minLength: 1,

        select: function(event, ui) {
            $('#find_text').val(ui.item.value);
            $('#search_form').submit();
        },
    });

    // control video play time
    $('.word-time').click(function(){
        var video = $(this).closest('.video-box-1').find('video')[0];
        var time = $(this).siblings('.sec-time').text();
        video.currentTime = time;
        video.play();
    });
});