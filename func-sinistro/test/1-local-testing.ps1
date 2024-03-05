curl -X POST -d '{"file_path": "1/Redes de proteção.jpeg"}' http://localhost:7071/api/gettext

curl -X POST -d '{"file_path": "1/Pedido 01.pdf"}' http://localhost:7071/api/gettext

curl -X POST -d '{"file_path": "1/Pedido 02.pdf"}' http://localhost:7071/api/gettext

curl -X POST -d '{"file_path": "1/uber-ida.pdf"}' http://localhost:7071/api/gettext

curl -X POST -d '{"text": "<p><p>Testing my function</br></p></p>"}' http://localhost:7071/api/removehtml

# files that possibly don't exist:

curl -X POST -d '{"file_path": "emails/Pedido 01.pdf"}' http://localhost:7071/api/gettext

curl -X POST -d '{"file_path": "/emails/2024-03-05T17:25:22 00:00-EMAIL TESTE-Felipe.Assis@microsoft.com/Pedido 01.pdf"}' http://localhost:7071/api/gettext

curl -X POST -d '{"file_path": "/emails/2024-03-05T18:38:02 00:00-EMAIL DE TESTE NOVO-Felipe.Assis@microsoft.com/image001.png"}' http://localhost:7071/api/gettext