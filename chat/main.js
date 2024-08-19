

function logar(){

    var login = document.getElementById('login').value;
    var senha = document.getElementById('senha').value;

    if(login == "Paulo" && senha == "12345678"){
        window.alert('LOGANDO....')
        location.href = "chat.html";
        localStorage.setItem('username', login);
     
    }
    else if(login == "Rafael" && senha == "12345679"){
        window.alert('LOGANDO....')
        location.href = "chat.html";
        localStorage.setItem('username', login);
    }
    else{
        window.alert('Usuario ou senha incorreta')
    }
}

var websocket;
var username;

function connectWebSocket() {
    websocket = new WebSocket("ws://localhost:8000");

    websocket.onopen = function () {
        console.log("Conexão estabelecida");
        username = localStorage.getItem('username');
        document.getElementById('username').textContent = username;
        websocket.send(username);
    };

    websocket.onmessage = function (event) {
        console.log("Mensagem recebida do servidor:", event.data);
        displayMessage(event.data);
    };

    websocket.onerror = function (event) {
        console.error("Erro ocorrido:", event);
    };

    websocket.onclose = function () {
        console.log("Conexão fechada");
    };
}

function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var message = messageInput.value.trim();

    if (message === "") {
        messageInput.placeholder = 'Digite algo antes...';
        return;
    }

    if (websocket.readyState === WebSocket.OPEN) {
        websocket.send(message);
        messageInput.value = ''; // Limpa o campo de entrada de mensagem
        displayMessage( `${username}: ` + message, true); // Exibe a mensagem enviada no lado direito
     
    } else {
        console.error("A conexão WebSocket não está aberta");
    }
}

function displayMessage(message, isSent) {
    var historic = document.getElementById('historic');
    var messageBox = document.createElement('div');
    var messageElement = document.createElement('p');
    messageElement.textContent = message;

    if (isSent) {
        messageElement.classList.add('sent'); // Adiciona a classe 'sent' para estilizar a mensagem enviada
    } else {
        messageElement.classList.add('received'); // Adiciona a classe 'received' para estilizar a mensagem recebida
    }
    messageBox.classList.add('message-box');
    messageBox.appendChild(messageElement);
    historic.appendChild(messageBox);
}

document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('btnEnviar');

    if(button) {
        connectWebSocket();
    
        button.addEventListener('click', sendMessage);
        document.getElementById('message_input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
});

function voltar(){
    location.href = "tela.html";
}