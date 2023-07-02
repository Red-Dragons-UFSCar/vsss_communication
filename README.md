# vsss_communication
Repositório criado para interface de comunicação utilizada na categoria Very Small Size Soccer VSSS

# Requisitos
* Python 3.8+
* Google protocol buffers (protoc v3.6.1)

# Instalação
Para utilização deste pacote de comunicação, é necessário realizar a instalação por meio dos seguintes comandos:

```bash
cd src
sudo python3 setup.py install
```

# Teste
A realização de testes são a partir dos arquivos do diretório examples. Em dois terminais diferentes, rode os códgos a seguir:


Terminal 1:
```bash
cd examples
python3 visao.py
```

Terminal 2:
```bash
cd examples
python3 controle.py
```

Terminal 3:
```bash
cd examples
python3 eletronica.py
```

A execução dos três terminais deve proporcionar para você o envio e recebimento de mensagens de todas as áreas. Caso algo esteja errado, uma mensagem de erro será exibida no terminal.
Nota-se também que os arquivos não precisam ser executados nesta ordem, em qualquer ordem eles vão funcionar como o esperado, desde que todos os arquivos sejam executados.
