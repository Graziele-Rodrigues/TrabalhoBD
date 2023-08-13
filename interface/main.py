import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
import customtkinter as ctk
import tkinter.messagebox as tkmb
from PIL import Image, ImageTk
import psycopg2
from conexaobd import Banco
from datetime import date

# selecionando o tema - dark, light , system (for system default)
ctk.set_appearance_mode("dark")
# selecionando cor tema - blue, green, dark-blue
ctk.set_default_color_theme("dark-blue")
# cria tkinter geral
app = ctk.CTk()
# configura fontes
title_font = ctk.CTkFont(family="sans-serif", size=20, slant="italic", weight="bold")
placeholder_botao = ctk.CTkFont(family="arial", size=15) 

class Faixas:
        def __init__(self, app, codigoBarras, album=False):
            self.app = app
            self.codigoBarras = codigoBarras
            self.fk_Album_fk_Produto_CodigoBarras = None  # Inicialmente, nenhum valor
            self.pessoaAdicionada = None  # Inicialmente, nenhuma pessoa foi adicionada
            self.generopk = None
            self.album = album
            self.escolheAlbumSingle()
        
        def get_pessoas(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()
            buscaPessoas = """ SELECT "CPF", "Nome" FROM "Pessoa"; """
            bd.execute(buscaPessoas)
            pessoas = bd.fetchall()
            bd.close() 
            return pessoas
        
        def get_listaGenero(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()
            buscaGeneros = """ SELECT "GeneroMusical" FROM "GeneroMusical"; """
            bd.execute(buscaGeneros)
            generos = bd.fetchall()
            bd.close() 
            return generos 
        

        def escolheAlbumSingle(self):
            telaCadastrarProd = ctk.CTkToplevel(app)
            telaCadastrarProd.title("Continuar cadastro")
            telaCadastrarProd.geometry("800x800")
            
            self.label = ctk.CTkLabel(telaCadastrarProd,text="Agora selecione o tipo de produto que foi cadastrado:", font=title_font)
            self.label.pack(pady=10)
        
            #frame
            self.frameCadastroProd = ctk.CTkFrame(master=telaCadastrarProd)
            self.frameCadastroProd.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)

            #botao CADASTRO SINGLE
            self.botaoCadastroProd = ctk.CTkButton(master=self.frameCadastroProd,text='Cadastrar SINGLE/FAIXA MUSICAL', width=150, font=placeholder_botao, command=self.cadastroFaixaSingle)
            self.botaoCadastroProd.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="ew") 

            #botao CADASTRO ALBUM
            self.botaoCadastroProd = ctk.CTkButton(master=self.frameCadastroProd,text='Cadastrar ALBUM', width=150, font=placeholder_botao, command=self.enviaAlbum)
            self.botaoCadastroProd.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
            self.botaoCadastroProd.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew") 


        def cadastroFaixaSingle(self):
            telaCadastrarSingle = ctk.CTkToplevel(app)
            telaCadastrarSingle.title("Cadastrar Single/Faixa Musical")
            telaCadastrarSingle.geometry("800x800")
            
            self.label = ctk.CTkLabel(telaCadastrarSingle,text="Cadastre o Single/Faixa Musical:", font=title_font)
            self.label.pack(pady=10)
        
            #frame
            self.frameCadastroSingle = ctk.CTkFrame(master=telaCadastrarSingle)
            self.frameCadastroSingle.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)
        
            # ISRC Label
            self.ISRCcLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Digite o ISRC", font=placeholder_botao)
            self.ISRCcLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
                
            # ISRC Entry Field
            self.ISRCcEntry = ctk.CTkEntry(master=self.frameCadastroSingle, placeholder_text="insira o ISRC", font=placeholder_botao, width=400)
            self.ISRCcEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # NOME Label
            self.nomesingleLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Nome", font=placeholder_botao)
            self.nomesingleLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
                
            # NOME Entry Field
            self.nomesingleEntry = ctk.CTkEntry(master=self.frameCadastroSingle, placeholder_text="insira o nome", font=placeholder_botao, width=400)
            self.nomesingleEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # TEMPO Label
            self.tempooLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Tempo", font=placeholder_botao)
            self.tempooLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
                
            # TEMPO DURACAO Entry Field
            self.tempooEntry = ctk.CTkEntry(master=self.frameCadastroSingle, placeholder_text="insira o tempo da faixa", font=placeholder_botao, width=400)
            self.tempooEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # FK_GENERO MUSICAL Label
            self.generoLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Gênero", font=placeholder_botao)
            self.generoLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
               
            # FK_GENERO MUSICAL Entry Field
            generos = self.get_listaGenero()
            generos_list = [genero[0] for genero in generos]  # Extrair os valores reais dos gêneros
            self.combo = ctk.CTkComboBox(master=self.frameCadastroSingle, values=generos_list)
            self.combo.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
            self.combo.set(generos_list[0])  # Defina o valor padrão
            
            # FAIXA MUSICAL Label
            self.faixaLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Faixa musical", font=placeholder_botao)
            self.faixaLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
                
            # FAIXA MUSICAL Entry Field
            self.faixaEntry = ctk.CTkEntry(master=self.frameCadastroSingle, placeholder_text="insira detalhes sobre a faixa", font=placeholder_botao, width=400)
            self.faixaEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
            
            pessoas = self.get_pessoas()
            pessoas_list = [pessoa[0] for pessoa in pessoas]  # Extrair pessoas

            pessoas = self.get_pessoas()
            pessoas_list = [f"{pessoa[0]} - {pessoa[1]}" for pessoa in pessoas]  # Extrair CPF e Nome

            # Autor MUSICAL Label
            self.autorLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Autor", font=placeholder_botao)
            self.autorLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

            # Autor Entry Field
            self.autor = ctk.CTkComboBox(master=self.frameCadastroSingle, values=pessoas_list)
            self.autor.grid(row=5, column=1, padx=20, pady=20, sticky="ew")
            self.autor.set(pessoas_list[0])  # Defina o valor padrão

            # Compositor MUSICAL Label
            self.compositorLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Compositor", font=placeholder_botao)
            self.compositorLabel.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

            # Compositor Entry Field
            self.compositor = ctk.CTkComboBox(master=self.frameCadastroSingle, values=pessoas_list)
            self.compositor.grid(row=6, column=1, padx=20, pady=20, sticky="ew")
            self.compositor.set(pessoas_list[0])  # Defina o valor padrão

            # Produtor Label
            self.produtorLabel = ctk.CTkLabel(master=self.frameCadastroSingle, text="Produtor Musical", font=placeholder_botao)
            self.produtorLabel.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

            # Produtor Label
            self.produtor = ctk.CTkComboBox(master=self.frameCadastroSingle, values=pessoas_list)
            self.produtor.grid(row=6, column=1, padx=20, pady=20, sticky="ew")
            self.produtor.set(pessoas_list[0])  # Defina o valor padrão

            # botao
            self.botaoCadastroPessoa = ctk.CTkButton(master=self.frameCadastroSingle,text='Cadastrar', width=250, font=placeholder_botao, command=self.enviaCadastroFaixaSingle)
            self.botaoCadastroPessoa.grid(row=7, column=0, columnspan=3, padx=20, pady=20, sticky="ew")


        def enviaCadastroFaixaSingle(self):
            banco = Banco()
            bd = banco.conexao.cursor()
            try:
                bd.execute(
                    "SELECT \"fk_Produto_CodigoBarras\" FROM public.\"Album\" WHERE \"fk_Produto_CodigoBarras\" = %s",
                    (self.codigoBarras,),
                )
                result = bd.fetchone()
                if result:
                    self.fk_Album_fk_Produto_CodigoBarras = result[0]

                bd.execute(
                    "SELECT \"GeneroMusical_PK\" FROM public.\"GeneroMusical\" WHERE \"GeneroMusical\" = %s",
                    (self.combo.get(),),
                )
                result = bd.fetchone()
                if result:
                    self.generopk = result[0]
                
                if not self.album:  # Verifique se não é um álbum (ou seja, é um single)
                    bd.execute("SELECT COUNT(*) FROM public.\"FaixaMusical_Single\" WHERE \"fk_Produto_CodigoBarras\" = %s", (self.codigoBarras,))
                    count = bd.fetchone()[0]

                    if count != 0:
                        tkmb.showerror(title="Erro", message="É um single, logo é permitido cadastrar apenas uma faixa")
                        return

                # Insere tabela FaixaMusical_Single
                sql = """INSERT INTO public."FaixaMusical_Single"("ISRC", "Nome", "TempoDuracao", "fk_GeneroMusical_GeneroMusical_PK", "FaixaMusical", "fk_Album_fk_Produto_CodigoBarras", "fk_Produto_CodigoBarras") VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                bd.execute(
                    sql,(self.ISRCcEntry.get(), self.nomesingleEntry.get(), self.tempooEntry.get(), self.generopk, self.faixaEntry.get(), self.fk_Album_fk_Produto_CodigoBarras, self.codigoBarras,),
                )
                banco.conexao.commit()

                # Insere tabela Participa_em
                self.autor_cpf = self.autor.get().split(' - ')[0]
                self.compositor_cpf = self.compositor.get().split(' - ')[0]
                self.produtor_cpf = self.produtor.get().split(' - ')[0]

                sql = """INSERT INTO public."Participa"("fk_Pessoa_CPF", "fk_FaixaMusical_Single_ISRC", "TipoPessoa") VALUES(%s,%s,%s)"""
                bd.execute(sql, (self.autor_cpf, self.ISRCcEntry.get(), "autor"),)
                banco.conexao.commit()
                bd.execute(sql, (self.compositor_cpf, self.ISRCcEntry.get(), "compositor"),)
                banco.conexao.commit()
                bd.execute(sql, (self.produtor_cpf, self.ISRCcEntry.get(), "produtor"),)
                banco.conexao.commit()

                bd.close()
                tkmb.showinfo(title="Cadastrado com Sucesso", message="Cadastro da faixa musical realizado com sucesso!",)

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                tkmb.showerror(
                    title="Erro",
                    message="Ocorreu um erro ao cadastrar a faixa musical.",
                )

            finally:
                if banco is not None:
                    pass
        

        def enviaAlbum(self):
            banco = Banco()  # Certifique-se de que a classe Banco esteja corretamente definida
            bd = banco.conexao.cursor()
            try:
                sql = """INSERT INTO public."Album"("fk_Produto_CodigoBarras") VALUES(%s)"""  
                bd.execute(sql, (self.codigoBarras, ))
                
                banco.conexao.commit()  # Commit as alterações no banco de dados
                bd.close()  # Feche a comunicação com o banco de dados
                tkmb.showinfo(title="Cadastrado Sucesso", message="Cadastro realizado com sucesso!")

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a inserção
                tkmb.showerror(title="Erro", message="Ocorreu um erro ao cadastrar o produto.")

            finally:
                if banco is not None:
                    self.album = True
                    self.cadastroFaixaSingle()
            
                   

class Produto:
        def __init__(self, app, cnpj):
            self.app = app
            self.cnpj = cnpj
            self.index()
              
        def cadastroPessoas(self):
            telaPessoas = ctk.CTkToplevel(self.app)  # Use self.app here
            telaPessoas.title("Deletar produto")
            telaPessoas.geometry("800x800")

            self.label = ctk.CTkLabel(telaPessoas, text="Verifique se a pessoa já existe em nosso sistema, caso não, crie", font=title_font)
            self.label.pack(pady=10)

            self.frameTelaCadastroPessoas = ctk.CTkFrame(master=telaPessoas)
            self.frameTelaCadastroPessoas.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)

            self.entry_consulta1 = ctk.CTkEntry(master=self.frameTelaCadastroPessoas, placeholder_text="Nome", width=300, font=("Arial", 12))
            self.entry_consulta1.grid(row=0, column=0, padx=30, pady=10, sticky="ew")

            self.entry_consulta2 = ctk.CTkEntry(master=self.frameTelaCadastroPessoas, placeholder_text="Cpf", width=300, font=("Arial", 12))
            self.entry_consulta2.grid(row=0, column=1, padx=30, pady=10, sticky="ew")

            self.btn_consultar = ctk.CTkButton(master=self.frameTelaCadastroPessoas, text="Consultar",  width=300, command=self.consultaDadosPessoas)
            self.btn_consultar.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

            self.btn_limpaConsulta = ctk.CTkButton(master=self.frameTelaCadastroPessoas, text="Limpa Consulta",  width=300, command=self.exibePessoas)
            self.btn_limpaConsulta.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

            self.btn_criaNovaPessoa = ctk.CTkButton(master=self.frameTelaCadastroPessoas, text="Nova Pessoa", width=600, command=self.criaNovaPessoa)
            self.btn_criaNovaPessoa.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="ew")

            self.exibePessoas()


        def exibePessoas(self):
            # Cria a tabela
            self.columns = ("Nome", "EmailContato", "RedeSocial")
            self.table = ttk.Treeview(master=self.frameTelaCadastroPessoas, columns=self.columns, show="headings", height=10)
            for col in self.columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center")  # Centraliza o conteúdo das células
            self.table.grid(row=3, column=0, columnspan=2, padx=30, pady=10, sticky="ew")

            # Aumenta a largura das colunas da tabela
            self.table.column("Nome", width=200)  # Ajuste a largura conforme necessário
            self.table.column("EmailContato", width=200)  # Ajuste a largura conforme necessário
            self.table.column("RedeSocial", width=200)  # Ajuste a largura conforme necessário

            # Estiliza o cabeçalho da tabela (nomes das colunas)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="blue")  # Define fonte em negrito e cor azul

            # Cria uma instância do banco
            banco = Banco()
            bd = banco.conexao.cursor()

            try:
                # Execute a consulta SQL para obter os dados das pessoas cadastradas
                sql = """SELECT "Nome", "EmailContato", "RedeSocial" FROM public."Pessoa" """
                bd.execute(sql)
                dados_pessoas = bd.fetchall()

                # Limpe a tabela antes de preencher novamente
                for item in self.table.get_children():
                    self.table.delete(item)

                # Preencha a tabela com os dados obtidos da consulta
                for pessoa in dados_pessoas:
                    self.table.insert("", "end", values=pessoa)

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a consulta

            finally:
                if banco is not None:
                    banco.conexao.close()
        
        def consultaDadosPessoas(self):
            filtro_nome = self.entry_consulta1.get()
            filtro_cpf = self.entry_consulta2.get()

            # Cria uma instância do banco
            banco = Banco()
            bd = banco.conexao.cursor()

            try:
                # Constrói a consulta SQL com filtros
                sql = """SELECT "Nome", "EmailContato", "RedeSocial" FROM public."Pessoa" WHERE """
                conditions = []

                if filtro_nome:
                    conditions.append(f'UPPER("Nome") LIKE UPPER(\'%{filtro_nome}%\')')

                if filtro_cpf:
                    conditions.append(f'UPPER("CPF") LIKE UPPER(\'%{filtro_cpf}%\')')

                if conditions:
                    sql += ' AND '.join(conditions)

                # Execute a consulta SQL
                bd.execute(sql)
                dados_pessoas = bd.fetchall()

                # Limpe a tabela antes de preencher novamente
                for item in self.table.get_children():
                    self.table.delete(item)

                # Preencha a tabela com os dados obtidos da consulta
                for pessoa in dados_pessoas:
                    self.table.insert("", "end", values=pessoa)

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a consulta

            finally:
                if banco is not None:
                    banco.conexao.close()


        def criaNovaPessoa(self):
                telaCriaNovaPessoa = ctk.CTkToplevel(app)
                telaCriaNovaPessoa.title("Cadastra nova pessoa")
                telaCriaNovaPessoa.geometry("800x800")

                self.label = ctk.CTkLabel(telaCriaNovaPessoa,text="Preencha os campos abaixo:", font=title_font)
                self.label.pack(pady=20)

                #frame
                self.frameCriaNovaPessoa = ctk.CTkFrame(master=telaCriaNovaPessoa)
                self.frameCriaNovaPessoa.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)

                # Nome Label
                self.namePessoaLabel = ctk.CTkLabel(master=self.frameCriaNovaPessoa, text="Nome", font=placeholder_botao)
                self.namePessoaLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
                # Nome Entry Field
                self.namePessoaEntry = ctk.CTkEntry(master=self.frameCriaNovaPessoa, placeholder_text="nome profissional", font=placeholder_botao, width=400)
                self.namePessoaEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # Email Label
                self.emailPessoaLabel = ctk.CTkLabel(master=self.frameCriaNovaPessoa, text="Email", font=placeholder_botao)
                self.emailPessoaLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
                # Email Entry Field
                self.emailPessoaEntry = ctk.CTkEntry(master=self.frameCriaNovaPessoa, placeholder_text="email principal", font=placeholder_botao, width=400)
                self.emailPessoaEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # CPF Label
                self.cpfPessoaLabel = ctk.CTkLabel(master=self.frameCriaNovaPessoa, text="CPF", font=placeholder_botao)
                self.cpfPessoaLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
                # CPF Entry Field
                self.cpfPessoaEntry = ctk.CTkEntry(master=self.frameCriaNovaPessoa, placeholder_text="cpf, apenas numeros (12345676522)", font=placeholder_botao, width=400)
                self.cpfPessoaEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # rede social Label
                self.redesocialPessoaLabel = ctk.CTkLabel(master=self.frameCriaNovaPessoa, text="Rede Social", font=placeholder_botao)
                self.redesocialPessoaLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
                # rede social Entry Field
                self.redesocialPessoaEntry = ctk.CTkEntry(master=self.frameCriaNovaPessoa, placeholder_text="Rede social - @", font=placeholder_botao, width=400)
                self.redesocialPessoaEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # botao
                self.botaoCadastroPessoa = ctk.CTkButton(master=self.frameCriaNovaPessoa,text='Cadastrar', width=250, font=placeholder_botao, command=self.enviaDadosPessoas)
                self.botaoCadastroPessoa.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        def enviaDadosPessoas(self):
                banco = Banco()
                bd = banco.conexao.cursor()
                try:
                    # Verifique se o CNPJ do usuário (fk_Usuario_CNPJ) existe na tabela "Usuario" antes de inserir na tabela "Pessoa"
                    bd.execute("SELECT COUNT(*) FROM public.\"Usuario\" WHERE \"CNPJ\" = %s", (self.cnpj,))
                    count = bd.fetchone()[0]

                    if count == 0:
                        tkmb.showerror(title="Erro", message="O CNPJ do usuário não existe na tabela 'Usuario'.")
                        return

                    # Execute a declaração INSERT
                    sql = """INSERT INTO public."Pessoa"("RedeSocial", "Nome", "EmailContato", "CPF", "fk_Usuario_CNPJ") VALUES(%s, %s, %s, %s, %s)"""
                    bd.execute(sql, (self.redesocialPessoaEntry.get(), self.namePessoaEntry.get(), self.emailPessoaEntry.get(), self.cpfPessoaEntry.get(), self.cnpj,))

                    # Confirme as alterações no banco de dados
                    banco.conexao.commit()

                    # Feche a comunicação com o banco de dados
                    bd.close()

                    # Exiba uma mensagem de sucesso
                    tkmb.showinfo(title="CadastradoSucesso", message="Cadastro realizado com sucesso!")

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    # Exiba uma mensagem de erro se houver algum problema com a inserção
                    tkmb.showerror(title="Erro", message="Ocorreu um erro ao cadastrar a pessoa.")

                finally:
                    if banco is not None:
                        banco.conexao.close()

        def get_distribuidora(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()
            buscaDistribuidora = """ SELECT "CNPJ", "Nome" FROM "PlataformaDigital"; """
            bd.execute(buscaDistribuidora)
            distribuidoras = bd.fetchall()
            bd.close() 
            return distribuidoras

        def cadastroProdutos(self):
                telaCadastrarProduto = ctk.CTkToplevel(app)
                telaCadastrarProduto.title("Cadastrar produto")
                telaCadastrarProduto.geometry("900x800")
            
                self.label = ctk.CTkLabel(telaCadastrarProduto,text="Cadastre o produto:", font=title_font)
                self.label.pack(pady=10)
        
                #frame
                self.frameCadastroProd = ctk.CTkFrame(master=telaCadastrarProduto)
                self.frameCadastroProd.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)
        
                # Código de barras Label
                self.codbarrasLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Código de barras", font=placeholder_botao)
                self.codbarrasLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
                
                # Código de barra Entry Field
                self.codbarrasEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira o codigo barras", font=placeholder_botao, width=400)
                self.codbarrasEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
                
                # Nome Label
                self.nameProdLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Nome", font=placeholder_botao)
                self.nameProdLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
                
                # Nome Entry Field
                self.nameProdEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="nome do álbum/single", font=placeholder_botao, width=400)
                self.nameProdEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        
                # Descrição capa Label
                self.capaLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Descrição visual de elementos da capa", font=placeholder_botao)
                self.capaLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
                    
                # Descrição capa Entry Field
                self.capaEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a descrição visual da capa", font=placeholder_botao, width=400)
                self.capaEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
                # Descrição Label
                self.descricaoLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Descrição", font=placeholder_botao)
                self.descricaoLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
                    
                # Descrição Entry Field
                self.descricaoEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a descrição do álbum/single", font=placeholder_botao, width=400)
                self.descricaoEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
               
                # Data de lançamento Label
                self.dataLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Data de lançamento", font=placeholder_botao)
                self.dataLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
                
                # Data de lançamento Entry Field
                self.dataEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a data (AAAA-MM-DD)", font=placeholder_botao, width=400)
                self.dataEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        
                # Idioma Label
                self.idiomaLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Idioma", font=placeholder_botao)
                self.idiomaLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
                    
                # Idioma Entry Field
                self.idiomaEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira o idioma do álbum/single", font=placeholder_botao, width=400)
                self.idiomaEntry.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                #Distribuidora 

                distribuidoras = self.get_distribuidora()
                distribuidoras_list = [f"{distribuidora[0]} - {distribuidora[1]}" for distribuidora in distribuidoras]  # Extrair pessoas
                #crie uma listBox para a distribuidora com select multiple
                self.distribuidoraLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Distribuidora", font=placeholder_botao)
                self.distribuidoraLabel.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

                self.distribuidora = Listbox(master=self.frameCadastroProd, selectmode=MULTIPLE, width=50, height=5)
                self.distribuidora.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
                for distribuidora in distribuidoras_list:
                    self.distribuidora.insert(END, distribuidora)
                self.distribuidora.select_set(0, END)  # Defina o valor padrão

                # botao de envio PRODUTO
                self.botaoCadastroProduto = ctk.CTkButton(master=self.frameCadastroProd,text='Cadastrar PRODUTO', width=150, font=placeholder_botao, command=self.enviaDadosProduto)
                self.botaoCadastroProduto.grid(row=7, column=0, columnspan=3, padx=20, pady=20, sticky="ew") 
                
        
        def enviaDadosProduto(self):
            banco = Banco()  # Certifique-se de que a classe Banco esteja corretamente definida
            bd = banco.conexao.cursor()
            try:
                try:
                    dataEntry = date.fromisoformat(self.dataEntry.get())
                except ValueError as error:
                     print(error)
                     tkmb.showerror(title="Erro", message="Data com formato errado.")
                     return
                
                # Verifique se o CNPJ do usuário (fk_Usuario_CNPJ) existe na tabela "Usuario" antes de inserir na tabela "Pessoa"
                bd.execute("SELECT COUNT(*) FROM public.\"Usuario\" WHERE \"CNPJ\" = %s", (self.cnpj,))
                count = bd.fetchone()[0]

                if count == 0:
                    tkmb.showerror(title="Erro", message="O CNPJ do usuário não existe na tabela 'Usuario'.")
                    return

                sql = """INSERT INTO public."Produto"("CodigoBarras", "Nome", "Capa", "Descricao", "Idioma", "DataLancamento", "fk_Usuario_Cnpj") VALUES(%s,%s,%s,%s,%s,%s,%s)"""  
                bd.execute(sql, (self.codbarrasEntry.get(), self.nameProdEntry.get(), self.capaEntry.get(), self.descricaoEntry.get(), self.idiomaEntry.get(), self.dataEntry.get(), self.cnpj,))
                
                distribuidoras = self.distribuidora.curselection()
                for distribuidora in distribuidoras:
                    bd.execute("INSERT INTO public.\"Distribuido\"(\"fk_PlataformaDigital_cnpj\", \"fk_Produto_CodigoBarras\") VALUES(%s,%s)", (self.distribuidora.get(distribuidora).split(" - ")[0],self.codbarrasEntry.get(),))
                banco.conexao.commit()  # Commit as alterações no banco de dados
                bd.close()  # Feche a comunicação com o banco de dados
                tkmb.showinfo(title="Cadastrado Sucesso", message="Cadastro realizado com sucesso!")

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                tkmb.showerror(title="Erro", message="Ocorreu um erro ao cadastrar o produto.")

            finally:
                if banco is not None:
                    Faixas(app, self.codbarrasEntry.get())
                    #conectando banco de dados
            

        def deletaProduto(self):
            telaDeletarProduto = ctk.CTkToplevel(app)
            telaDeletarProduto.title("Deletar produto")
            telaDeletarProduto.geometry("800x800")

            self.label = ctk.CTkLabel(telaDeletarProduto,text="Preencha os campos abaixo:", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameDeletaProduto = ctk.CTkFrame(master=telaDeletarProduto)
            self.frameDeletaProduto.pack(pady=20, padx=40, fill='both', expand=True)

            # Codigo Barras Label
            self.codigoBarrasLabel = ctk.CTkLabel(master=self.frameDeletaProduto, text="Código de barras", font=placeholder_botao)
            self.codigoBarrasLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

            # CodigoBarras Entry Field
            self.codigoBarrasEntry = ctk.CTkEntry(master=self.frameDeletaProduto, placeholder_text="Digite o código de barras do produto", font=placeholder_botao, width=400)
            self.codigoBarrasEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            #botão para procurar os produtos
            self.botaoProcurarProduto = ctk.CTkButton(master=self.frameDeletaProduto,text='Procurar produto', width=250, font=placeholder_botao, command=self.enviaCodigoBarrasDelete)
            self.botaoProcurarProduto.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        

        def enviaCodigoBarrasDelete(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()

            # realiza busca
            buscaCodigoBarras = """ SELECT "CodigoBarras" FROM public."Produto" where "CodigoBarras" = %s and "fk_Usuario_Cnpj" = %s; """
            bd.execute(buscaCodigoBarras, (self.codigoBarrasEntry.get(), self.cnpj))
            self.buscaCodigoBarras = bd.fetchone()

            # fecha comunicação com banco
            bd.close()

            if self.buscaCodigoBarras:
                self.mostrarProdutoDelete()
            else:
                tkmb.showerror(title="Erro", message="Não há nenhum produto com esse código de barras!")


        def mostrarProdutoDelete(self):
            telaMostrarProdutoDelete = ctk.CTkToplevel(app)
            telaMostrarProdutoDelete.title("Produto encontrado")
            telaMostrarProdutoDelete.geometry("800x800")

            self.label = ctk.CTkLabel(telaMostrarProdutoDelete,text="Produto encontrado! Certeza que deseja excluir?", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameDeletaProduto = ctk.CTkFrame(master=telaMostrarProdutoDelete)
            self.frameDeletaProduto.pack(pady=20, padx=40, fill='both', expand=True)

            #botão para para deletar produto
            self.botaoDeletarProduto = ctk.CTkButton(master=self.frameDeletaProduto,text='Deletar produto', width=250, font=placeholder_botao, command=self.deletarProduto)
            self.botaoDeletarProduto.grid(row=1, column=3, columnspan=3, padx=10, pady=20, sticky="ew")           


        def deletarProduto(self):
            try:
                # conectando banco de dados
                banco = Banco()
                bd = banco.conexao.cursor()
                
                # realiza busca
                deleteProduto = """ DELETE FROM public."Produto" where "CodigoBarras" = %s and "fk_Usuario_Cnpj" = %s; """
                bd.execute(deleteProduto, (self.codigoBarrasEntry.get(), self.cnpj,))
                banco.conexao.commit()

                # fecha comunicação com banco
                bd.close()

                # Mensagem de sucesso
                tkmb.showinfo(title="Deletado com sucesso", message="Produto deletado com sucesso!")
            except Exception as e:
                    # Em caso de erro, mostra a mensagem de erro
                    tkmb.showerror(title="Erro", message="Ocorreu um erro ao deletar o produto: " + str(e))


        def visualizarRelatorios(self):
            telaRelatorios = ctk.CTkToplevel(app)
            telaRelatorios.title("Relatórios")
            telaRelatorios.geometry("800x800")

            self.label = ctk.CTkLabel(telaRelatorios,text="Consultar dados", font=title_font)
            self.label.pack(pady=10)

            self.botaoFaixa = ctk.CTkButton(master=telaRelatorios,text='Consultar faixa', width=250, font=placeholder_botao, command=self.consultarFaixa)
            self.botaoFaixa.pack(pady=10,padx=10)

            self.botaoAlbum = ctk.CTkButton(master=telaRelatorios,text='Consultar album', width=250, font=placeholder_botao, command=self.consultarAlbum)
            self.botaoAlbum.pack(pady=10,padx=10)

            self.botaoArtista = ctk.CTkButton(master=telaRelatorios,text='Consultar artista', width=250, font=placeholder_botao, command=self.consultarArtista)
            self.botaoArtista.pack(pady=10,padx=10)

        
        def consultarFaixa(self):
            telaConsultarFaixa = ctk.CTkToplevel(app)
            telaConsultarFaixa.title("Consultar reproduções de uma faixa")
            telaConsultarFaixa.geometry("800x800")

            self.label = ctk.CTkLabel(telaConsultarFaixa,text="Consultar reproduções de uma faixa", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameConsultarFaixa = ctk.CTkFrame(master=telaConsultarFaixa)
            self.frameConsultarFaixa.pack(pady=20, padx=40, fill='both', expand=True)

            # ISRC Label
            self.isrcLabel = ctk.CTkLabel(master=self.frameConsultarFaixa, text="ISRC", font=placeholder_botao)
            self.isrcLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

            # ISRC Entry Field
            self.isrcEntry = ctk.CTkEntry(master=self.frameConsultarFaixa, placeholder_text="Digite o ISRC da faixa", font=placeholder_botao, width=400)
            self.isrcEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            #botão para procurar as faixas
            self.botaoProcurarFaixa = ctk.CTkButton(master=self.frameConsultarFaixa,text='Procurar faixa', width=250, font=placeholder_botao, command=self.enviarIsrc)
            self.botaoProcurarFaixa.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        def enviarIsrc(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()

            # realiza busca
            buscaIsrc = """ SELECT SUM(DISTINCT "QuantidadeReproducao") FROM public."Reproduzida" where "fk_FaixaMusical_Single_ISRC" = %s; """
            bd.execute(buscaIsrc, (self.isrcEntry.get(),))
            self.buscaIsrc = bd.fetchone()

            #realiza segunda busca 
            buscaReproducoes = """ SELECT P."Nome", R."QuantidadeReproducao", R."QuantidadeReproducao" * P."ValorPagoReproducao" as valor_reproducao
                                    FROM public."Reproduzida" as R
                                    JOIN public."PlataformaDigital" as P ON R."fk_PlataformaDigital_cnpj" = P."CNPJ"
                                    WHERE R."fk_FaixaMusical_Single_ISRC" = %s; """
            bd.execute(buscaReproducoes, (self.isrcEntry.get(),))
            self.buscaReproducoes = bd.fetchall()
            
            numeroReproducoes = self.buscaIsrc[0]

            # fecha comunicação com banco
            bd.close()

            if self.buscaIsrc:
                self.mostrarFaixa(numeroReproducoes, self.buscaReproducoes)
            else:
                tkmb.showerror(title="Erro", message="Não há nenhuma faixa com esse ISRC!")


        def mostrarFaixa(self, numeroReproducoes, buscaReproducoes):
            telaMostrarFaixa = ctk.CTkToplevel(app)
            telaMostrarFaixa.title("Faixa encontrada")
            telaMostrarFaixa.geometry("800x800")

            #mostrar o resultado da busca
            self.label = ctk.CTkLabel(telaMostrarFaixa,text="Faixa encontrada! Número de reproduções: " + str(numeroReproducoes), font=title_font)
            self.label.pack(pady=10)

            for i in range(len(buscaReproducoes)):
                self.label = ctk.CTkLabel(telaMostrarFaixa,text="Plataforma: '" + str(buscaReproducoes[i][0]) + "' - Número de reproduções: " + str(buscaReproducoes[i][1]) + " - Valor: R$" + str(buscaReproducoes[i][2]), font=title_font)
                self.label.pack(pady=10)


        def consultarAlbum(self):
            telaConsultarAlbum = ctk.CTkToplevel(app)
            telaConsultarAlbum.title("Consultar número de reproduções de um album")
            telaConsultarAlbum.geometry("800x800")

            self.label = ctk.CTkLabel(telaConsultarAlbum,text="Consultar número de reproduções de um album", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameConsultarAlbum = ctk.CTkFrame(master=telaConsultarAlbum)
            self.frameConsultarAlbum.pack(pady=20, padx=40, fill='both', expand=True)
            
            # Codigo Barras Label
            self.codigoBarrasLabel = ctk.CTkLabel(master=self.frameConsultarAlbum, text="Código de barras", font=placeholder_botao)
            self.codigoBarrasLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

            # CodigoBarras Entry Field
            self.codigoBarrasEntry = ctk.CTkEntry(master=self.frameConsultarAlbum, placeholder_text="Digite o código de barras do album", font=placeholder_botao, width=400)
            self.codigoBarrasEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            #botão para procurar os produtos
            self.botaoProcurarAlbum = ctk.CTkButton(master=self.frameConsultarAlbum,text='Procurar album', width=250, font=placeholder_botao, command=self.enviarCodigoBarrasAlbum)
            self.botaoProcurarAlbum.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        def enviarCodigoBarrasAlbum(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()

            # realiza busca
            buscaCodigoBarras = """ SELECT SUM(DISTINCT "QuantidadeReproducao") FROM public."Reproduzida" where "fk_FaixaMusical_Single_fk_Produto_CodigoBarras" = %s; """
            bd.execute(buscaCodigoBarras, (self.codigoBarrasEntry.get(),))
            self.buscaCodigoBarras = bd.fetchone()

            #realiza segunda busca 
            buscaReproducoes = """ SELECT P."Nome", R."QuantidadeReproducao", R."QuantidadeReproducao" * P."ValorPagoReproducao" as valor_reproducao
                                    FROM public."Reproduzida" as R
                                    JOIN public."PlataformaDigital" as P ON R."fk_PlataformaDigital_cnpj" = P."CNPJ"
                                    WHERE R."fk_FaixaMusical_Single_fk_Produto_CodigoBarras" = %s; """
            bd.execute(buscaReproducoes, (self.codigoBarrasEntry.get(),))
            self.buscaReproducoes = bd.fetchall()
            

            numeroReproducoes = self.buscaCodigoBarras[0]

            # fecha comunicação com banco
            bd.close()

            if self.buscaCodigoBarras:
                self.mostrarAlbum(numeroReproducoes, self.buscaReproducoes)
            else:
                tkmb.showerror(title="Erro", message="Não há nenhum album com esse código de barras!")
        

        def mostrarAlbum(self, numeroReproducoes, buscaReproducoes):
            telaMostrarAlbum = ctk.CTkToplevel(app)
            telaMostrarAlbum.title("Album encontrado")
            telaMostrarAlbum.geometry("800x800")

            #mostrar o resultado da busca
            self.label = ctk.CTkLabel(telaMostrarAlbum,text="Album encontrado! Número de reproduções: " + str(numeroReproducoes), font=title_font)
            self.label.pack(pady=10)

            for i in range(len(buscaReproducoes)):
                self.label = ctk.CTkLabel(telaMostrarAlbum,text="Plataforma: '" + str(buscaReproducoes[i][0]) + "' - Número de reproduções: " + str(buscaReproducoes[i][1]) + " - Valor: R$" + str(buscaReproducoes[i][2]), font=title_font)
                self.label.pack(pady=10)
        

        def consultarArtista(self):
            telaConsultarArtista = ctk.CTkToplevel(app)
            telaConsultarArtista.title("Consultar número de reproduções de um artista")
            telaConsultarArtista.geometry("800x800")

            self.label = ctk.CTkLabel(telaConsultarArtista,text="Consultar número de reproduções de um artista", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameConsultarArtista = ctk.CTkFrame(master=telaConsultarArtista)
            self.frameConsultarArtista.pack(pady=20, padx=40, fill='both', expand=True)
            
            # cpf Label
            self.cpfLabel = ctk.CTkLabel(master=self.frameConsultarArtista, text="CPF", font=placeholder_botao)
            self.cpfLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

            # cpf Entry Field
            self.cpfEntry = ctk.CTkEntry(master=self.frameConsultarArtista, placeholder_text="Digite o cpf do artista", font=placeholder_botao, width=400)
            self.cpfEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            #botão para procurar os produtos
            self.botaoProcurarArtista = ctk.CTkButton(master=self.frameConsultarArtista,text='Procurar artista', width=250, font=placeholder_botao, command=self.enviarCpfArtista)
            self.botaoProcurarArtista.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


        def enviarCpfArtista(self):
            # conectando banco de dados
            banco = Banco()
            bd = banco.conexao.cursor()

            # realiza busca
            buscaCpf = """ SELECT SUM(DISTINCT "QuantidadeReproducao") 
            FROM public."Reproduzida", public."Participa"
            where "fk_Pessoa_CPF" = %s and "TipoPessoa" = 'autor' """
            bd.execute(buscaCpf, (self.cpfEntry.get(),))
            self.buscaCpf = bd.fetchone()

            numeroReproducoes = self.buscaCpf[0]

            # fecha comunicação com banco
            bd.close()

            if self.buscaCpf:
                self.mostrarArtista(numeroReproducoes)
            else:
                tkmb.showerror(title="Erro", message="Não há nenhum artista com esse nome!")

        def mostrarArtista(self, numeroReproducoes):
            telaMostrarArtista = ctk.CTkToplevel(app)
            telaMostrarArtista.title("Artista encontrado")
            telaMostrarArtista.geometry("800x800")

            #mostrar o resultado da busca
            self.label = ctk.CTkLabel(telaMostrarArtista,text="Artista encontrado! Número de reproduções: " + str(numeroReproducoes), font=title_font)
            self.label.pack(pady=10)


        def exibeProdutos(self):
            # Cria a tabela
            self.columns = ("Codigo Barras", "Nome", "Lançamento", "Idioma")
            self.table = ttk.Treeview(master=self.frameIndex3, columns=self.columns, show="headings", height=10)
            for col in self.columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center")  # Centraliza o conteúdo das células
            self.table.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky="ew")

            # Aumenta a largura das colunas da tabela
            self.table.column("Codigo Barras", width=200)  # Ajuste a largura conforme necessário
            self.table.column("Nome", width=200)  # Ajuste a largura conforme necessário
            self.table.column("Lançamento", width=200)  # Ajuste a largura conforme necessário
            self.table.column("Idioma", width=200)  # Ajuste a largura conforme necessário

            # Estiliza o cabeçalho da tabela (nomes das colunas)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="blue")  # Define fonte em negrito e cor azul

            # Cria uma instância do banco
            banco = Banco()
            bd = banco.conexao.cursor()

            try:
                # Execute a consulta SQL para obter os dados produtos cadastrados daquele usuario
                bd.execute("SELECT \"CodigoBarras\", \"Nome\", \"DataLancamento\", \"Idioma\" FROM public.\"Produto\" WHERE \"fk_Usuario_Cnpj\" = %s", (self.cnpj,))
                dados_produtos = bd.fetchall()

                # Limpe a tabela antes de preencher novamente
                for item in self.table.get_children():
                    self.table.delete(item)

                # Preencha a tabela com os dados obtidos da consulta
                for produto in dados_produtos:
                    codigo_barras, nome, lancamento, idioma = produto
                    self.table.insert("", "end", values=(codigo_barras, nome, lancamento, idioma))

                 # Bind the item selection event to a function
                    self.table.bind("<ButtonRelease-1>", self.on_item_select)

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a consulta

            finally:
                if banco is not None:
                    banco.conexao.close()

        
        def on_item_select(self, event):
            selected_item = self.table.focus()
            if selected_item:
                item = self.table.item(selected_item)
                codigo_barras = item['values'][0]  # Assuming the barcode is the first column in the table
                self.exibeFaixas(codigo_barras)


        def exibeFaixas(self, codigoBarras):
            self.codigo = str(codigoBarras)
            telaExibeFaixas = ctk.CTkToplevel(app)
            telaExibeFaixas.title("Faixas do produto: ")
            telaExibeFaixas.geometry("800x800")

            self.label = ctk.CTkLabel(telaExibeFaixas,text="Consultar número de reproduções de um artista", font=title_font)
            self.label.pack(pady=10)

            #frame
            self.frameExibeFaixas = ctk.CTkFrame(master=telaExibeFaixas)
            self.frameExibeFaixas.pack(pady=20, padx=40, fill='both', expand=True)

            # Cria a tabela
            self.columns = ("ISCR", "Nome", "Autor", "Compositor", "Produtor")
            self.table = ttk.Treeview(master=self.frameExibeFaixas, columns=self.columns, show="headings", height=10)
            for col in self.columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center")  # Centraliza o conteúdo das células
            self.table.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky="ew")

            # Aumenta a largura das colunas da tabela
            self.table.column("ISCR", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Nome", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Autor", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Compositor", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Produtor", width=150)  # Ajuste a largura conforme necessário

            # Estiliza o cabeçalho da tabela (nomes das colunas)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="blue")  # Define fonte em negrito e cor azul

            banco = Banco()
            bd = banco.conexao.cursor()
            try:
                bd.execute("SELECT \"ISRC\", \"Nome\" FROM public.\"FaixaMusical_Single\" WHERE \"fk_Produto_CodigoBarras\" = %s", (self.codigo,))
                dados_faixas = bd.fetchall()

                sql = """SELECT "Nome" FROM public."Participa" pa
                        JOIN public."Pessoa" ON "CPF" = pa."fk_Pessoa_CPF" 
                        WHERE pa."TipoPessoa" = 'autor' AND pa."fk_FaixaMusical_Single_ISRC" IN (
                            SELECT "ISRC"
                            FROM public."FaixaMusical_Single"
                            WHERE "fk_Produto_CodigoBarras" = %s
                        );"""

                bd.execute(sql, (self.codigo, ))
                self. autor = bd.fetchall()

                sql = """SELECT "Nome" FROM public."Participa" pa
                        JOIN public."Pessoa" ON "CPF" = pa."fk_Pessoa_CPF" 
                        WHERE pa."TipoPessoa" = 'compositor' AND pa."fk_FaixaMusical_Single_ISRC" IN (
                            SELECT "ISRC"
                            FROM public."FaixaMusical_Single"
                            WHERE "fk_Produto_CodigoBarras" = %s
                        );"""

                bd.execute(sql, (self.codigo, ))
                self.compositor = bd.fetchall()

                sql = """SELECT "Nome" FROM public."Participa" pa
                        JOIN public."Pessoa" ON "CPF" = pa."fk_Pessoa_CPF" 
                        WHERE pa."TipoPessoa" = 'autor' AND pa."fk_FaixaMusical_Single_ISRC" IN (
                            SELECT "ISRC"
                            FROM public."FaixaMusical_Single"
                            WHERE "fk_Produto_CodigoBarras" = %s
                        );"""

                bd.execute(sql, (self.codigo, ))
                self.produtor = bd.fetchall()

                # Limpe a tabela antes de preencher novamente
                for item in self.table.get_children():
                    self.table.delete(item)

                # Preencha a tabela com os dados obtidos da consulta
                count = 0
                for faixas in dados_faixas:
                    isrc, nome = faixas
                    self.table.insert("", "end", values=(isrc, nome, self.autor[count], self.compositor[count], self.compositor[count]))
                    count=count+1
                    
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a consulta

            finally:
                if banco is not None:
                    banco.conexao.close()

        def index(self):
            index = ctk.CTkToplevel(app)
            index.geometry("800x800")
            index.title("Tela inicial")

            # Criar a imagem
            self.my_image = Image.open("interface/image/logo.png")
            self.my_image = ImageTk.PhotoImage(self.my_image.resize((150, 150)))  # Resize the image
            self.image_label = ctk.CTkLabel(index, image=self.my_image, text="")
            self.image_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

            # Criar o rótulo
            self.label = ctk.CTkLabel(index, text="Distribuidora digital de música", font=title_font)
            self.label.grid(row=0, column=1, padx=20, pady=20, sticky="w")
            #  Criar frame
            self.frameIndex = ctk.CTkFrame(master=index)
            self.frameIndex.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="ew")
            # Criar os botões
            self.botaoArtista = ctk.CTkButton(master=self.frameIndex, text='Cadastrar pessoas', width=250, font=placeholder_botao, command=self.cadastroPessoas)
            self.botaoArtista.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            self.botaoRelatorio = ctk.CTkButton(master=self.frameIndex, text='Relatorios', width=250, font=placeholder_botao, command=self.visualizarRelatorios)
            self.botaoRelatorio.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

            # Cria Frame
            self.frameIndex2 = ctk.CTkFrame(master=index)
            self.frameIndex2.grid(row=2, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

            # Criar o botão para cadastrar produto
            self.btn_cadastraProduto = ctk.CTkButton(master=self.frameIndex2, text="Cadastrar produto", width=175, font=placeholder_botao, command=self.cadastroProdutos)
            self.btn_cadastraProduto.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
   
            # Criar o botão para deletar produtos
            self.btn_deletaProduto = ctk.CTkButton(master=self.frameIndex2, text="Deletar produto", width=175, font=placeholder_botao, command=self.deletaProduto)
            self.btn_deletaProduto.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

            # botao de atualizar meus produtos
            self.botaoCadastroProduto = ctk.CTkButton(master=self.frameIndex2,text='Atualizar produtos', width=150, font=placeholder_botao, command=self.exibeProdutos)
            self.botaoCadastroProduto.grid(row=1, column=2, columnspan=3, padx=20, pady=20, sticky="ew") 

            # Cria Frame
            self.frameIndex3 = ctk.CTkFrame(master=index)
            self.frameIndex3.grid(row=3, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

            self.exibeProdutos()

            
class Usuario:
    def __init__(self, app):
        self.app = app
        self.telaLogin()

    def login(self):
        # conectando banco de dados
        banco = Banco()
        bd = banco.conexao.cursor()

        # realiza busca
        buscaCnpj = """ SELECT "CNPJ" FROM public."Usuario" where "CNPJ" = %s; """
        buscaSenha = """ SELECT "Senha" FROM public."Usuario" where "CNPJ" = %s; """
        bd.execute(buscaCnpj, (self.user_entry.get(),))
        self.username = bd.fetchone()

        bd.execute(buscaSenha, (self.user_entry.get(),))
        self.password = bd.fetchone()

        # fecha comunicação com banco
        bd.close()

        # testando credenciais
        if self.username and self.password and self.user_pass.get() == self.password[0]:
            # Oculta a janela de login
            app.withdraw()
            self.cnpj = self.username
            Produto(app, self.cnpj)

        elif self.username and self.user_pass.get() != self.password[0]:
            tkmb.showwarning(title='Senha incorreta', message='Senha incorreta')
        else:
            tkmb.showerror(title="Falha no login", message="usuário e senha incorretos")
            
    def telaLogin(self):
            app.geometry("800x800")
            self.app.title("Login distribuidora musical")
            self.label = ctk.CTkLabel(app,text="Seja bem vindo a sua distribuidora de música digital!", font=title_font)
            self.label.pack(pady=20)

            self.frame = ctk.CTkFrame(master=app)
            self.frame.pack(pady=20, padx=40, fill='both', expand=True)

            self.my_image = Image.open("interface/image/logo.png")
            self.my_image = ImageTk.PhotoImage(self.my_image.resize((200, 200)))  # Resize the image
            self.image_label = ctk.CTkLabel(master=self.frame, image=self.my_image, text="")
            self.image_label.pack(pady=0, padx=0)

            self.label = ctk.CTkLabel(master=self.frame, text='')
            self.label.pack(pady=12, padx=10)

            self.user_entry= ctk.CTkEntry(master=self.frame,placeholder_text="CNPJ", width=250, font=placeholder_botao)
            self.user_entry.pack(pady=12,padx=10)

            self.user_pass= ctk.CTkEntry(master=self.frame,placeholder_text="Senha",show="*", width=250, font=placeholder_botao)
            self.user_pass.pack(pady=12,padx=10)

            self.button = ctk.CTkButton(master=self.frame,text='Entrar', width=250, font=placeholder_botao, command=self.login)
            self.button.pack(pady=12,padx=10)

            self.button = ctk.CTkButton(master=self.frame,text='Novo cadastro', width=250, font=placeholder_botao, command=self.cadastro)
            self.button.pack(pady=12,padx=10)

            self.checkbox = ctk.CTkCheckBox(master=self.frame,text='Esqueci minha senha')
            self.checkbox.pack(pady=12,padx=10)
    

    def enviaDadosUsuarios(self):
        #conectando banco de dados
        banco = Banco()
        bd = banco.conexao.cursor()
        try:
            # execute the INSERT statement
            sql = """INSERT INTO public."Usuario"("Nome", "Email", "Senha", "CNPJ", "DadosBancario") VALUES(%s,%s,%s,%s,%s)"""
            bd.execute(sql, (self.nameEntry.get(), self.emailEntry.get(), self.senhaEntry.get(), self.cnpjEntry.get(), self.bancoEntry.get()))
            # commit the changes to the database
            banco.conexao.commit()
            # close communication with the database
            bd.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if banco is not None:
                tkmb.showinfo(title="CadastradoSucesso", message="Cadastro realizado com sucesso!")


    def cadastro(self):
            telaCadastro = ctk.CTkToplevel(app)
            telaCadastro.title("Tela Cadastro")
            telaCadastro.geometry("800x800")

            self.label = ctk.CTkLabel(telaCadastro,text="Cadastre seus dados:", font=title_font)
            self.label.pack(pady=20)
            #frame
            self.frameCadastro = ctk.CTkFrame(master=telaCadastro)
            self.frameCadastro.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)

            # Nome Label
            self.nameLabel = ctk.CTkLabel(master=self.frameCadastro, text="Nome", font=placeholder_botao)
            self.nameLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            # Nome Entry Field
            self.nameEntry = ctk.CTkEntry(master=self.frameCadastro, placeholder_text="nome profissional", font=placeholder_botao, width=400)
            self.nameEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # Email Label
            self.emailLabel = ctk.CTkLabel(master=self.frameCadastro, text="Email", font=placeholder_botao)
            self.emailLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
            # Email Entry Field
            self.emailEntry = ctk.CTkEntry(master=self.frameCadastro, placeholder_text="email principal", font=placeholder_botao, width=400)
            self.emailEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # Senha Label
            self.senhaLabel = ctk.CTkLabel(master=self.frameCadastro, text="Senha", font=placeholder_botao)
            self.senhaLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
             # Senha Entry Field
            self.senhaEntry = ctk.CTkEntry(master=self.frameCadastro, placeholder_text="senha", font=placeholder_botao, width=400)
            self.senhaEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # CNPJ Label
            self.cnpjLabel = ctk.CTkLabel(master=self.frameCadastro, text="CNPJ", font=placeholder_botao)
            self.cnpjLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
            # CNPJ Entry Field
            self.cnpjEntry = ctk.CTkEntry(master=self.frameCadastro, placeholder_text="apenas números (12345678000100)", font=placeholder_botao, width=400)
            self.cnpjEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

            # dados bancarios Label
            self.bancoLabel = ctk.CTkLabel(master=self.frameCadastro, text="Dados Bancarios", font=placeholder_botao)
            self.bancoLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
            # dados bancarios Entry Field
            self.bancoEntry = ctk.CTkEntry(master=self.frameCadastro, placeholder_text="n° conta, n° banco, n° agencia", font=placeholder_botao, width=400)
            self.bancoEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
            
            # botao
            self.botaoCadastro = ctk.CTkButton(master=self.frameCadastro,text='Cadastrar', width=250, font=placeholder_botao, command=self.enviaDadosUsuarios)
            self.botaoCadastro.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

    # def todosProdutos(self): 
         


if __name__ == "__main__":
    Usuario(app)

#inicia aplicação tkinter
app.mainloop()
#testa
