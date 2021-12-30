document.querySelector("#submit").onclick = function(e){
    const messageInputDom = document.querySelector('#input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message':message,
    }));
    messageInputDom.value = '';
}



const roomName = JSON.parse(document.getElementById('room-name').textContent);
console.log(roomName)
const chatSocket = new WebSocket(
    'ws://'+
    window.location.host+
    '/ws/chat/'+
    roomName+
    '/'
);

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data)
    console.log(data)
    document.querySelector('#user-hello').textContent = (data.tester);
    document.querySelector('#chat-text').value += (data.message + '\n');
}