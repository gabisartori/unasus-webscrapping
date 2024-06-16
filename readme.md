<!-- Esse é um arquivo markdown, se você está lendo esse texto -->
<!-- Tente abrir o arquivo com um leitor de markdown apropriado -->
<!-- Se não tiver um leitor, abra o arquivo readme.html no navegador -->

# Requisitos
Para o funcionamento do programa, é necessário que os seguintes itens estejam ok
- [Python versão 3.8+](#python)
- [Biblioteca Selenium instalada](#selenium)
- [Driver para o browser](#driver)
- [Configuração do script](#configuração)

Caso todos os requisitos estejam ok, basta executar o programa
```
python main.py
```
# Python
O interpretador do python é necessário para execução do script e pode ser instalado seguindo o [tutorial oficial](https://wiki.python.org/moin/BeginnersGuide/Download). Apesar de já vir instalado em alguns sistemas operacionais.

Para verificar se o interpretador está instalado, abra o terminal e digite
```
python --version
```
ou
```
python3 --version
```
O resultado deve ser `Python 3.8` ou uma versão superior. Caso o resultado diga que o programa não está instalado, siga o tutorial para instalá-lo.

É esperado que o gerenciador de pacotes "pip" seja instalado junto do interpretador. Você pode verificar se foi instalado de fato digitando no terminal
```
pip --version
```
ou
```
pip3 --version
```
Se nenhuma das duas der como resultado uma versão instalada. Siga o [tutorial oficial](https://pip.pypa.io/en/stable/installation/) para instalá-lo, pois ele será usado no próximo passo.

[Voltar para requisitos](#requisitos)

# Selenium
Tendo uma versão do Python e o gerenciador de pacotes Pip instalados no sistema, é preciso instalar a biblioteca Selenium para que o script possa executar.
```
pip install selenium
```

[Voltar para requisitos](#requisitos)

# Driver
A biblioteca selenium depende do programa Geckodriver para poder interagir com o Firefox.

Cada sistema operacional tem sua sequência de passos para a instalação do Geckodriver

## Windows
[Tutorial aqui](https://www.browserstack.com/guide/geckodriver-selenium-python)

[Voltar para requisitos](#requisitos)

## Linux
1. Baixe o binário adequado para a sua máquina na [Página de lançamentos](https://github.com/mozilla/geckodriver/releases)
1. Descompacte o arquivo
1. Permita que o arquivo seja executado como um programa
```
chmod +x ./geckodriver
```
1. Mova o arquivo para a pasta de programas instalados (/usr/local/bin)
```
sudo mv ./geckodriver /user/local/bin/
```
ps. Certifique-se de que ambos os comandos estão sendo executados na pasta em que o arquivo binário foi descompactado

[Voltar para requisitos](#requisitos)

## MacOS
No terminal, execute
```
brew install geckodriver
```

[Voltar para requisitos](#requisitos)

# Configuração
Informações como login e senha do usuário devem ser preenchidas no arquivo config.txt para que o programa possa acessar as páginas que contém os relatórios.
Informações configuráveis:

- Url do curso
- Login
- Senha
- Número de grupos
- Pasta para donwload (opcional)

#### O arquivo segue o seguinte formato:
```
url: http://site.com
login: seu_id_ufsc
password: sua_senha
numero de grupos: numero_de grupos
pasta para download: /caminho/para/a/pasta/destino/
```
É importante respeitar a ordem dos itens

[Voltar para requisitos](#requisitos)