curl -X POST -d '{"directory": "638459383340000000"}' http://localhost:7071/api/prepare01

curl -X POST -d '{"directory": "638459383340000000", "question": "Quantos aparelhos foram comprados?"}' http://localhost:7071/api/validate01

curl -X POST -d '{"directory": "638459383340000000", "question": "Qual endereço de instalação da rede de proteção?"}' http://localhost:7071/api/validate01