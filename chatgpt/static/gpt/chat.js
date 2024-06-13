document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatContent = document.getElementById('chat-content');
    const questionInput = document.getElementById('question');
    const scrollToBottomButton = document.getElementById('scroll-to-bottom'); // 추가

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const userMessage = questionInput.value;
        if (userMessage.trim() === '') {
            return;
        }

        // 사용자 메시지를 채팅창에 추가
        addMessage(userMessage, 'user-message');

        // 서버에 메시지 전송
        fetch(chatForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams(new FormData(chatForm))
        })
        .then(response => response.json())
        .then(data => {
            // 서버 응답 메시지를 채팅창에 추가
            addMessage(data.result, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // 입력 필드 초기화
        questionInput.value = '';
    });

    function addMessage(message, className) {
        // 새로운 메시지 요소 생성
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', className);
        messageElement.textContent = message;

        // chat-content 요소에 메시지 추가
        chatContent.appendChild(messageElement);

        // chat-content의 스크롤을 최신 메시지로 이동
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    // 추가
    // chat-content 스크롤 이벤트 감지 및 버튼 표시/숨기기
    chatContent.addEventListener('scroll', () => {
        if (chatContent.scrollTop < chatContent.scrollHeight - chatContent.clientHeight - 100) {
            scrollToBottomButton.classList.add('show');
        } else {
            scrollToBottomButton.classList.remove('show');
        }
    });
    
    // 맨 아래로 스크롤하는 함수
    window.scrollToBottom = function() {
        chatContent.scrollTop = chatContent.scrollHeight;
    };

    // text-button 요소를 가져옵니다.
    const textButton = document.getElementById('text-button');

    // text-button을 클릭했을 때 실행할 함수를 정의합니다.
    textButton.addEventListener('click', function() {
        // question textarea 요소를 가져옵니다.
        const questionTextarea = document.getElementById('question');

        // question textarea의 높이를 초기값(여기서는 50px)으로 설정합니다.
        questionTextarea.style.height = '50px';
    });
});
