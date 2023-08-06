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
telaCadastro = ctk.CTk()
telaCadastroPessoas = ctk.CTk()
# configura fontes
title_font = ctk.CTkFont(family="sans-serif", size=20, slant="italic", weight="bold")
placeholder_botao = ctk.CTkFont(family="arial", size=15) 

class Produto:
        def __init__(self, app, cnpj):
            self.app = app
            self.cnpj = cnpj
            self.index()
              
        def cadastroPessoas(self):
            telaCadastroPessoas = ctk.CTkToplevel(app)
            telaCadastroPessoas.geometry("800x800")
            telaCadastroPessoas.title("CadastroPessoas")

            # Criar a imagem
            self.my_image = Image.open("interface/image/logo.png")
            self.my_image = ImageTk.PhotoImage(self.my_image.resize((150, 150)))  # Resize the image
            self.image_label = ctk.CTkLabel(telaCadastroPessoas, image=self.my_image, text="")
            self.image_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

            # Criar o rótulo
            self.label = ctk.CTkLabel(telaCadastroPessoas, text="Distribuidora digital de música", font=title_font)
            self.label.grid(row=0, column=1, padx=20, pady=20, sticky="w")
            # Criar frame
            self.frameTelaProduto = ctk.CTkFrame(master=telaCadastroPessoas)
            self.frameTelaProduto.grid(row=1, column=0, columnspan=2, padx=40, pady=20, sticky="ew")
            # Criar os botões
            self.botaoProduto = ctk.CTkButton(master=self.frameTelaProduto, text='Produtos', width=250, font=placeholder_botao, command=self.cadastroProdutos)
            self.botaoProduto.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            self.botaoRelatorio = ctk.CTkButton(master=self.frameTelaProduto, text='Relatorios', width=250, font=placeholder_botao, command=self.visualizarRelatorios)
            self.botaoRelatorio.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

            # Cria Frame
            self.frameTelaProduto2 = ctk.CTkFrame(master=telaCadastroPessoas)
            self.frameTelaProduto2.grid(row=2, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

            # Criar o widget de caixa de consulta
            self.entry_consulta1 = ctk.CTkEntry(master=self.frameTelaProduto2, placeholder_text="Nome", width=200, font=("Arial", 12))
            self.entry_consulta1.grid(row=0, column=0, padx=30, pady=10, sticky="ew")

            # Criar o widget de caixa de consulta
            self.entry_consulta2 = ctk.CTkEntry(master=self.frameTelaProduto2, placeholder_text="Cnpj", width=200, font=("Arial", 12))
            self.entry_consulta2.grid(row=0, column=1, padx=30, pady=10, sticky="ew")

            # Criar o botão para consultar
            self.btn_consultar = ctk.CTkButton(master=self.frameTelaProduto2, text="Consultar", command=self.consultarDadosPessoas)
            self.btn_consultar.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

            # Criar o botão para criarNovaPessoa
            self.btn_criaPessoa = ctk.CTkButton(master=self.frameTelaProduto2, text="Nova Pessoa", command=self.criaNovaPessoa)
            self.btn_criaPessoa.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

            # Cria Frame
            self.frameTelaProduto3 = ctk.CTkFrame(master=telaCadastroPessoas)
            self.frameTelaProduto3.grid(row=3, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

            # Exibe Tabela com resultados
            self.columns = ("Nome", "EmailContato", "RedeSocial")
            self.table = ttk.Treeview(master=self.frameTelaProduto3, columns=self.columns, show="headings", height=10)
            for col in self.columns:
                self.table.heading(col, text=col)
            self.table.grid(row=0, column=0, padx=30, pady=10, sticky="ew")


        def criaNovaPessoa(self):
                telaCriaNovaPessoa = ctk.CTkToplevel(app)
                telaCriaNovaPessoa.title("Cadastra nova pessoa")
                telaCriaNovaPessoa.geometry("800x800")

                self.label = ctk.CTkLabel(telaCriaNovaPessoa,text="Preencha os campos abaixo:", font=title_font)
                self.label.pack(pady=20)

                #frame
                self.frameCriaNovaPessoa = ctk.CTkFrame(master=telaCriaNovaPessoa)
                self.frameCriaNovaPessoa.pack(pady=20, padx=40, fill='both', expand=True)

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

        def consultarDadosPessoas(self):
             pass
        
        def cadastroProdutos(self):
             pass
        
        def editaProdutos(self):
             pass
        
        def deletaProduto(self):
            telaDeletarProduto = ctk.CTkToplevel(app)
            telaDeletarProduto.title("Deletar produto")
            telaDeletarProduto.geometry("700x300")

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
            buscaCodigoBarras = """ SELECT "CodigoBarras" FROM public."Produto" where "CodigoBarras" = %s; """
            bd.execute(buscaCodigoBarras, (self.codigoBarrasEntry.get(),))
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
            telaMostrarProdutoDelete.geometry("700x200")

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
                deleteProduto = """ DELETE FROM public."Produto" where "CodigoBarras" = %s; """
                bd.execute(deleteProduto, (self.codigoBarrasEntry.get(),))
                banco.conexao.commit()

                # fecha comunicação com banco
                bd.close()

                # Mensagem de sucesso
                tkmb.showinfo(title="Deletado com sucesso", message="Produto deletado com sucesso!")
            except Exception as e:
                    # Em caso de erro, mostra a mensagem de erro
                    tkmb.showerror(title="Erro", message="Ocorreu um erro ao deletar o produto: " + str(e))



        def visualizarRelatorios(self):
             pass
        
        
        def index(self):
            index = ctk.CTkToplevel(app)
            index.geometry("1000x1000")
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
            self.botaoArtista = ctk.CTkButton(master=self.frameIndex, text='Cadastrar artistas', width=250, font=placeholder_botao, command=self.cadastroPessoas)
            self.botaoArtista.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
            self.botaoRelatorio = ctk.CTkButton(master=self.frameIndex, text='Relatorios', width=250, font=placeholder_botao, command=self.visualizarRelatorios)
            self.botaoRelatorio.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

            # Cria Frame
            self.frameIndex2 = ctk.CTkFrame(master=index)
            self.frameIndex2.grid(row=2, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

            # Criar o botão para cadastrar produto
            self.btn_cadastraProduto = ctk.CTkButton(master=self.frameIndex2, text="Cadastrar produto", command=self.cadastroProdutos)
            self.btn_cadastraProduto.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

            # Criar o botão para editar produto
            self.btn_editaProduto = ctk.CTkButton(master=self.frameIndex2, text="Editar produto", command=self.editaProdutos)
            self.btn_editaProduto.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

            # Criar o botão para deletar produtos
            self.btn_deletaProduto = ctk.CTkButton(master=self.frameIndex2, text="Deletar produto", command=self.deletaProduto)
            self.btn_deletaProduto.grid(row=1, column=1, padx=30, pady=10, sticky="ew")

           

            
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
            app.geometry("700x700")
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
            telaCadastro.geometry("700x700")

            self.label = ctk.CTkLabel(telaCadastro,text="Cadastre seus dados:", font=title_font)
            self.label.pack(pady=20)
            #frame
            self.frameCadastro = ctk.CTkFrame(master=telaCadastro)
            self.frameCadastro.pack(pady=20, padx=40, fill='both', expand=True)

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
telaCadastro.mainloop()
telaCadastroPessoas.mainloop()