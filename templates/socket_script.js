window.onload = function(){
    function addToChat(msg){
        const span = document.createElement("span");
        const chat = document.querySelector(".chat");
        if (msg.nome === "{{session.user}}"){
            span.className = "message_mine"
        }
        else{
            span.className = "message"
        }
        span.innerHTML = `<strong>${msg.nome}:</strong> ${msg.message} <span class="time">${msg.time}</span>`
        chat.append(span);
    }
    const uri = window.location.origin
    const socket = io(uri);

    socket.on('conect', () => {
        socket.send('usuario conectado')
    });

    document.querySelector('form').addEventListener("submit", function(){
        event.preventDefault();
        socket.emit('sendMessage', {nome: event.target[0].value, message: event.target[1].value})

        event.target[1].value = "";
    });

    socket.on('getMsg', (msg) => {
        addToChat(msg);
        var heightPage = document.body.scrollHeight;
        window.scrollTo(0 , heightPage);
    });
}
