# Distribuidora digital de música

Sistema para cadastro de produtos musicais a serem distribuídos. O usuário da nossa plataforma são produtores fonográficos, ou seja, quem detém o direito de um produto- album musical, como por exemplo gravadoras.

## 🚀 Descrição

1. Tela de cadastro e login usuários. Os usuários são os produtores fonográficos dos álbum. É de responsabilidade deles cadastrar os produtos e também as pessoas que participam desse produto. Para cadastro do usuário guardamos o seguinte: 
    - Nome
    - Email
    - Senha
    - CNPJ
    - dadosBancarios

2. Tela cadastro de pessoas. Todo usuário do sistema pode cadastrar uma pessoa se ela não estiver ainda no banco. As pessoas assumem papel nas faixas musicais. Guardamos as seguintes informações dela:
    - Nome
    - Email
    - CPF
    - Rede social
    - Telefone

3. Cadastro de produtos
    - Código de barras deve ser único por produto
    - Um produto pode ser single, o qual deve ter apenas uma faixa. E também ser um álbum que pode ter n faixas musicais. Cada faixa musical deve ter um ISCR único, além de guardar a informação do autor, compositor e produtor musical. 

 
4. Visualização dos ganhos recebidos por produto ou faixas

5. Capacidade deletar

<img src="/img/conceitual.png">
<img src="/img/logico.png">

### 📋 Pré-requisitos

1. VsCode ou outro editor como pycharm -  [Baixe vsCode aqui ](https://code.visualstudio.com/download)
2. python 3.x.x - [Baixe python aqui](http://www.sis4.com/brModelo/)
3. pip - pacote gerenciamento padrão
4. SGBD - pgAdmin ou Dbeaver -  [Baixe pgAdmin aqui](https://www.pgadmin.org/)

### 🔧 Instalação

Instalação biblioteca tkinter:

```
pip3 install tk
```

Verificar se foi instalado corretamente, use o seguinte código em um arquivo.py

```
import tkinter
tkinter._test()
```

Instalação biblioteca customTkinter:

```
pip3 install customtkinter
```

Instalação biblioteca conexão PostgreSQL:

```
pip3 install psycopg2
```


## ⚙️ Executanando os testes e mostrando seus resultados
1. Cadastro Usuário 
<img src="/img/cadastroUsuario.png">
<img src="/img/SenhaIncorreta.png">
<img src="/img/tabelaUsuario.png">

2. Cadastro de Pessoas
<img src="/img/pessoas.PNG">
<img src="/img/cadastro-pessoa.PNG">
<img src="/img/pesquisar-pessoa.PNG">

3. Cadastro de Produtos 
<img src="/img/cadastro-produto.PNG">
<img src="/img/cadastro-album-sucesso.PNG">
<img src="/img/cadastro-single-faixa-musical.PNG">

4. Visualizar produtos e faixas daquele usuário
<img src="/img/tela-inicial.PNG">

5. Visualizar relatórios
<img src="/img/RELATORIOS.PNG">
<img src="/img/reproducoes-faixa.PNG">
<img src="/img/relatorios-faixa.PNG">
<img src="/img/reproducoes-album.PNG">
<img src="/img/relatorio-album.PNG">
<img src="/img/relatorio-artista.PNG">
<img src="/img/relatorio-artista-mostrar.PNG">

6. Deletar

<img src="/img/procurar-produto-delete.PNG">
<img src="/img/sucesso-procura-delete.PNG">



## 📦 Implantação

```
python main.py
```


## 🛠️ Construído com

* [BrModelo](http://www.sis4.com/brModelo/) - Software para construir modelo conceitual ER e lógico
* [ElephantSQL](https://www.elephantsql.com/) - Banco de Dados PostgreSQL como serviço
* [Tkinter](https://rometools.github.io/rome/) - Biblioteca python para desenvolver interface gráfica


## ✒️ Autores



* **Graziele** - *Desenvolvedora* - [GitHub Graziele](https://github.com/Graziele-Rodrigues)
* **Gessica** - *Desenvolvedora* - [GitHub Gessica](https://github.com/linkParaPerfil)
* **Laura** - *Desenvolvedora* -  [GitHub Laura](https://github.com/LauraMarques20)
* **Luisa** - *Desenvolvedora* - [GitHub Luisa](https://github.com/linkParaPerfil)
.



---
⌨️ com ❤️ por (Discentes Universidade Federal Ouro Preto) 😊