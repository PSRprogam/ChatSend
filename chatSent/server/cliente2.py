import websocket
import threading

def on_message(ws, message):
    print("Mensagem recebida do servidor:", message)

def on_error(ws, error):
    print("Erro ocorrido:", error)

def on_close(ws):
    print("Conexão fechada")

def on_open(ws):
    print("Conexão estabelecida")

    # Inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(ws,))
    receive_thread.start()

def receive_messages(ws):
    # Loop para receber mensagens do servidor
    while True:
        message = ws.sock.recv()
        print("Mensagem recebida de outro cliente:", message.decode())

def send_message(ws):
    # Loop para enviar mensagens do cliente para o servidor
    while True:
        message = input("Digite uma mensagem para enviar ao servidor (ou 'sair' para encerrar): ")
        if message == "sair":
            break
        ws.send(message)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8000",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Inicia uma thread para enviar mensagens do cliente para o servidor
    send_thread = threading.Thread(target=send_message, args=(ws,))
    send_thread.start()

    ws.run_forever()
