window.onload = function(){
    function addToChat(msg){
        const span = document.createElement("span");
        const chat = document.querySelector(".chat");
        span.className = determinaClasseDependendoDoEmissor(msg.nome)
        span.innerHTML = determinaLayoutDaMensagem(msg)
        chat.append(span);
    }

    function determinaClasseDependendoDoEmissor(usuario){
        if (usuario === "{{session.user}}"){
            return "message_mine"
        }
        else{
            return "message"
        }
    }

    function determinaLayoutDaMensagem(msg){
        if (ehAdmin()){
            return  `<strong>${msg.nome}:</strong> ${msg.message} <span class="time">${msg.time}</span>
                <a class="delete" href="deletar/${msg.indice}">deletar</a>`
        }else{
            return `<strong>${msg.nome}:</strong> ${msg.message} <span class="time">${msg.time}</span>`
        }

    }

    function ehAdmin(){
        console.log("{{ session.admin }}" === "True")
        return "{{ session.admin }}" === "True"
    }

    const uri = window.location.origin
    const socket = io(uri);

    document.querySelector('form').addEventListener("submit", function(){
        event.preventDefault();
        socket.emit('sendMessage', {nome: event.target[0].value, message: event.target[1].value})

        event.target[1].value = "";
    });

    socket.on('getMsg', (msg) => {
        addToChat(msg);
        rolaParaFinalDaPagina()
    });

    function rolaParaFinalDaPagina(){
        var heightPage = document.body.scrollHeight;
        window.scrollTo(0 , heightPage);
    }
}
