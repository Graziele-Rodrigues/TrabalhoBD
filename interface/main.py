import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import tkinter.messagebox as tkmb
from PIL import Image, ImageTk
import psycopg2
from conexaobd import Banco

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
        def __init__(self, app, codigoBarras):
            self.app = app
            self.codigoBarras = codigoBarras

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

        
        def cadastroProdutos(self):
                telaCadastrarProduto = ctk.CTkToplevel(app)
                telaCadastrarProduto.title("Cadastrar produto")
                telaCadastrarProduto.geometry("800x800")
            
                self.label = ctk.CTkLabel(telaCadastrarProduto,text="Cadastre o produto:", font=title_font)
                self.label.pack(pady=10)
        
                #frame
                self.frameCadastroProd = ctk.CTkFrame(master=telaCadastrarProduto)
                self.frameCadastroProd.pack(pady=20, padx=40, fill='both', anchor=tk.CENTER, expand=True)
        
                # Código de barras Label
                self.codbarrasLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Código de barras", font=placeholder_botao)
                self.codbarrasLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
                
                # Código de barra Entry Field
                self.codbarrasEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira o codigo barras", font=placeholder_botao, width=400)
                self.codbarrasEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
                
                # Nome Label
                self.nameProdLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Nome", font=placeholder_botao)
                self.nameProdLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
                
                # Nome Entry Field
                self.nameProdEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="nome do álbum/single", font=placeholder_botao, width=400)
                self.nameProdEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        
                # Descrição capa Label
                self.capaLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Descrição visual de elementos da capa", font=placeholder_botao)
                self.capaLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
                    
                # Descrição capa Entry Field
                self.capaEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a descrição visual da capa", font=placeholder_botao, width=400)
                self.capaEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
    
                # Descrição Label
                self.descricaoLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Descrição", font=placeholder_botao)
                self.descricaoLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
                    
                # Descrição Entry Field
                self.descricaoEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a descrição do álbum/single", font=placeholder_botao, width=400)
                self.descricaoEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
               
                # Data de lançamento Label
                self.dataLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Data de lançamento", font=placeholder_botao)
                self.dataLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
                
                # Data de lançamento Entry Field
                self.dataEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira a data", font=placeholder_botao, width=400)
                self.dataEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        
                # Idioma Label
                self.idiomaLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="Idioma", font=placeholder_botao)
                self.idiomaLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
                    
                # Idioma Entry Field
                self.idiomaEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira o idioma do álbum/single", font=placeholder_botao, width=400)
                self.idiomaEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # cnpj usuario Label
                self.cnpjusuarioLabel = ctk.CTkLabel(master=self.frameCadastroProd, text="cnpj do usuario", font=placeholder_botao)
                self.cnpjusuarioLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
                    
                # cnpj usuaario Entry Field
                self.cnpjusuarioEntry = ctk.CTkEntry(master=self.frameCadastroProd, placeholder_text="insira o cnpj de usuario", font=placeholder_botao, width=400)
                self.cnpjusuarioEntry.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

                # botao de envio
                self.botaoCadastroProduto = ctk.CTkButton(master=self.frameCadastroProd,text='Cadastrar', width=250, font=placeholder_botao, command=self.enviaDadosProduto)
                self.botaoCadastroProduto.grid(row=6, column=1, columnspan=3, padx=20, pady=20, sticky="ew") 
                
                self.exibeProdutos()

        
        def enviaDadosProduto(self):
                banco = Banco()  
                bd = banco.conexao.cursor()

                buscarCodigoBarras = """ SELECT "CodigoBarras" FROM public."Produto" where "CodigoBarras" = %s; """
                bd.execute(buscarCodigoBarras, (self.codbarrasEntry.get(),))
                self.buscarCodigoBarras = bd.fetchone()
                
                if self.buscarCodigoBarras:
                        tkmb.showerror(title="Mensagem", message="Este produto já foi cadastrado")
                        bd.close()  # Feche a comunicação com o banco de dados

                else:
                        try:
                                sql = """INSERT INTO public."Produto"("CodigoBarras", "Nome", "Capa", "Descricao", "Idioma", "DataLancamento", "fk_Usuario_CNPJ") VALUES(%s,%s,%s,%s,%s,%s,%s)"""  
                                bd.execute(sql, (self.codbarrasEntry.get(), self.nameProdEntry.get(), self.capaEntry.get(), self.descricaoEntry.get(), self.idiomaEntry.get(), self.dataEntry.get(), self.cnpjusuarioEntry.get()))
                    
                                banco.conexao.commit()  # Commit as alterações no banco de dados
                                bd.close()  # Feche a comunicação com o banco de dados

                                tkmb.showinfo(title="CadastradoSucesso", message="Cadastro realizado com sucesso!")

                        except (Exception, psycopg2.DatabaseError) as error:
                                print(error)
                                tkmb.showerror(title="Erro", message="Ocorreu um erro ao cadastrar o produto.")

        
        def exibeProdutos(self):
            # Cria a tabela
            self.columns = ("CodigoBarras", "Nome", "Lançamento", "Ações")
            self.table = ttk.Treeview(master=self.frameCadastro, columns=self.columns, show="headings", height=10)
            for col in self.columns:
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center")  # Centraliza o conteúdo das células
            self.table.grid(row=7, column=0, columnspan=2, padx=30, pady=10, sticky="ew")

            # Aumenta a largura das colunas da tabela
            self.table.column("CodigoBarras", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Nome", width=200)  # Ajuste a largura conforme necessário
            self.table.column("Lançamento", width=150)  # Ajuste a largura conforme necessário
            self.table.column("Ações", width=100)  # Ajuste a largura conforme necessário

            # Estiliza o cabeçalho da tabela (nomes das colunas)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="blue")  # Define fonte em negrito e cor azul

            # Cria uma instância do banco
            banco = Banco()
            bd = banco.conexao.cursor()

            try:
                # Remova os espaços em branco do CNPJ
                cnpj = self.cnpj[0].strip()
                # Execute a consulta SQL para obter os dados dos produtos cadastrados
                bd.execute("SELECT \"CodigoBarras\", \"Nome\", \"DataLancamento\" FROM public.\"Produto\" WHERE \"fk_Usuario_Cnpj\" = %s", (cnpj,))
                dados_produtos = bd.fetchall()
                
                # Limpe a tabela antes de preencher novamente
                for item in self.table.get_children():
                    self.table.delete(item)

    
                # Preencha a tabela com os dados obtidos da consulta 
                for produto in dados_produtos:
                    codigo_barras, nome, lancamento = produto
                    self.table.insert("", "end", values=(codigo_barras, nome, lancamento, ""))
                    button = ctk.CTkButton(self.table, text="Ação", command=Faixas(app, codigo_barras))
                    self.table.window_create("", window=button, padx=10, pady=5)

            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                # Exiba uma mensagem de erro se houver algum problema com a consulta

            finally:
                if banco is not None:
                    banco.conexao.close()


        def editaProdutos(self):
            telaEditarProduto = ctk.CTkToplevel(app)
            telaEditarProduto.title("Editar produto")
            telaEditarProduto.geometry("800x800")
            
            self.label = ctk.CTkLabel(telaEditarProduto,text="Preencha os campos abaixo:", font=title_font)
            self.label.pack(pady=10)

        
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
            where "fk_Pessoa_CPF" = %s and "TipoPessoa" = 'Artista' """
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


        def index(self):
            index = ctk.CTkToplevel(app)
            index.geometry("800x800")
            index.title("Tela inicial")

            # Criar a imagem
            # self.my_image = Image.open("image/logo.png")
            # self.my_image = ImageTk.PhotoImage(self.my_image.resize((150, 150)))  # Resize the image
            # self.image_label = ctk.CTkLabel(index, image=self.my_image, text="")
            # self.image_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")


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

            # Criar o botão para editar produto
            self.btn_editaProduto = ctk.CTkButton(master=self.frameIndex2, text="Editar produto", width=175, font=placeholder_botao, command=self.editaProdutos)
            self.btn_editaProduto.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

            # Criar o botão para deletar produtos
            self.btn_deletaProduto = ctk.CTkButton(master=self.frameIndex2, text="Deletar produto", width=175, font=placeholder_botao, command=self.deletaProduto)
            self.btn_deletaProduto.grid(row=1, column=2, padx=30, pady=10, sticky="ew")

            
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

            # self.my_image = Image.open("image/logo.png")
            # self.my_image = ImageTk.PhotoImage(self.my_image.resize((200, 200)))  # Resize the image
            # self.image_label = ctk.CTkLabel(master=self.frame, image=self.my_image, text="")
            # self.image_label.pack(pady=0, padx=0)

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
