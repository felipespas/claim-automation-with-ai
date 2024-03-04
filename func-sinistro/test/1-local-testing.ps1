curl -X POST -d '{"file_path": "1/Redes de proteção.jpeg", "file_type": "image"}' http://localhost:7071/api/validacaoinicial

curl -X POST -d '{"file_path": "1/Pedido 01.pdf", "file_type": "pdf"}' http://localhost:7071/api/validacaoinicial

curl -X POST -d '{"file_path": "1/Pedido 02.pdf", "file_type": "pdf"}' http://localhost:7071/api/validacaoinicial

curl -X POST -d '{"text": "<p><p>Testing my function</br></p></p>"}' http://localhost:7071/api/removehtml



