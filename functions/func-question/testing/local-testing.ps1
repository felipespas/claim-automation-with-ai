curl -X POST -d '{"directory": "638464433540000000"}' http://localhost:7071/api/prepare01

curl -X POST -d '{"directory": "638464433540000000", "question": "Quantos aparelhos foram comprados?"}' http://localhost:7071/api/validate01

curl -X POST -d '{"directory": "638464433540000000", "question": "Qual endereço de instalação da rede de proteção?"}' http://localhost:7071/api/validate01

curl -X POST -d '{"directory": "ExampleData"}' http://localhost:7071/api/prepare01

curl -X POST -d '{"directory": "lab1"}' http://localhost:7071/api/prepare01

curl -X POST -d '{"directory": "001", "question": "Quem é Felipe de Assis?"}' http://localhost:7071/api/question01