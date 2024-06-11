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
        // 메시지 컨테이너 요소 생성
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('chat-message-container');

        // bot-message일 경우 프로필 이미지를 추가
        if (className === 'bot-message') {
            const svgElement = document.createElement('img');
            svgElement.src = 'static/gpt/image/ai.svg'; // 봇 이미지의 경로로 변경
            svgElement.alt = 'Bot';
            svgElement.classList.add('bot-image'); // 스타일링을 위한 클래스 추가

            // 메시지 컨테이너에 이미지 추가
            messageContainer.appendChild(svgElement);
        }

        // 새로운 메시지 요소 생성
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', className);
        messageElement.textContent = message;

        // 메시지 컨테이너에 메시지 요소 추가
        messageContainer.appendChild(messageElement);

        // chat-content 요소에 메시지 컨테이너 추가
        chatContent.appendChild(messageContainer);

        // chat-content의 스크롤을 최신 메시지로 이동
        chatContent.scrollTop = chatContent.scrollHeight;
    }
    
});
