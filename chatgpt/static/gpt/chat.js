document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatContent = document.getElementById('chat-content');
    const questionInput = document.getElementById('question');

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
});
