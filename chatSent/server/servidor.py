import asyncio
import websockets

# Armazena as conexões ativas
connected_clients = set()

# Dicionário para mapear as conexões aos respectivos usuários
client_users = {}

# Função que será chamada ao receber uma nova conexão
async def websocket_handler(websocket, path):
    # Adiciona a nova conexão à lista de conexões ativas
    connected_clients.add(websocket)
    print("Nova conexão estabelecida")

    try:
        # Recebe o nome de usuário do cliente
        username = await websocket.recv()
        print("Usuário conectado:", username)

        # Armazena a conexão e o usuário no dicionário de clientes
        client_users[websocket] = username

        # Envia mensagem de boas-vindas ao cliente
        welcome_message = f"Bem-vindo, {username}!"
        await websocket.send(welcome_message)

        # Loop para receber e enviar mensagens
        while True:
            message = await websocket.recv()
            print("Mensagem recebida do cliente:", message)

            # Encontra o usuário remetente
            sender_username = client_users[websocket]

            # Envia a mensagem recebida para o cliente destino
            await send_message_to_client(message, sender_username, websocket)


    finally:
        # Remove a conexão da lista de conexões ativas ao ser fechada
        connected_clients.remove(websocket)
        del client_users[websocket]
        print("Conexão fechada")

async def send_message_to_client(message, sender_username, sender_websocket):
    # Encontra todas as conexões ativas, exceto a conexão remetente
    recipient_websockets = [client for client in connected_clients if client != sender_websocket]

    # Envia a mensagem para todos os clientes destinatários
    for client in recipient_websockets:
        if client in client_users:  # Verifica se a conexão existe no dicionário client_users
            recipient_username = client_users[client]
            formatted_message = f"{sender_username}: {message}"
            await client.send(formatted_message)


# Função que inicia o servidor WebSocket
async def start_server():
    async with websockets.serve(websocket_handler, 'localhost', 8000):
        print("Servidor WebSocket iniciado na porta 8000")
        await asyncio.Future()  # Mantém o servidor em execução indefinidamente

# Inicia o loop de eventos do asyncio
asyncio.get_event_loop().run_until_complete(start_server())
asyncio.get_event_loop().run_forever()
