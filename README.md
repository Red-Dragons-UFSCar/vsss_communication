# vsss_communication
Repositório criado para interface de comunicação utilizada na categoria Very Small Size Soccer VSSS

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
python3 eletronica.py
```

Terminal 2:
```bash
cd examples
python3 controle.py
```

Enquanto o arquivo controle.py não enviar nenhuma informação, o arquivo eletronica manterá a velocidade recebida em 0. Entretanto, quando o controle.py é iniciado, a velocidade 10 é recebida.
