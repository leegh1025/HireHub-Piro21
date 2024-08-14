function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    // POST
    $(document).on('submit', '#comment-form', function(event){
        event.preventDefault();

        var applicantId = $('#load-comment').data('applicant-id');
        console.log(applicantId);
        var url = applicantId + "/comment/";
        console.log($('#comment-form').serialize())

        $.ajax({
            url: url, //$('#comment-form').attr('action'), // 폼의 액션 URL을 사용
            type: 'POST',
            data: $('#comment-form').serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(data) {
                console.log('Server response:', data); // 응답 데이터 로그 출력
                if (data.success) {
                    $('#comment_list').append(
                        `<div class="comment"><small><strong>작성자:</strong> ${data.comment.interviewer}</small><p>| ${data.comment.text}</p></div>`
                    );
                    $('#id_text').val(''); // 입력 필드를 비웁니다.
                } else {
                    alert(data.error);
                    console.error(data.form_errors); // 폼 오류 메시지 출력
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX request failed: ' + error);
            }
        });
    })
})

$(document).ready(function() {
    // 코멘트 삭제
    $(document).on('click', '.deleteCommentBtn', function() {
        if (!confirm('정말로 이 질문을 삭제하시겠습니까?')) {
            return;
        }

        var commentId = $(this).data('comment-id');
        var applicantId = $('#load-comment').data('applicant-id');
        var url = applicantId + "/comment/" + commentId + "/delete/";

        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(data) {
                if (data.success) {
                    $('.comment[data-comment-id="' + commentId + '"]').remove();
                } else {
                    alert('Failed to delete question: ' + data.error);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred: ' + error);
                console.error('AJAX request failed:', error);
            }
        });
    });
});