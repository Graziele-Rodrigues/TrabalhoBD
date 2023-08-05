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
telaCadastroProduto = ctk.CTk()
# configura fontes
title_font = ctk.CTkFont(family="sans-serif", size=20, slant="italic", weight="bold")
placeholder_botao = ctk.CTkFont(family="arial", size=15) 

class Produto:
        def __init__(self, app):
            self.app = app
            self.cadastrarProdutos()
              
        def cadastrarProdutos(self):
            
            telaCadastroProduto = ctk.CTkToplevel(app)
            telaCadastroProduto.geometry("700x700")
            telaCadastroProduto.title("Produtos")
            label = ctk.CTkLabel(telaCadastroProduto,text="Cadastre aqui os produtos e veja seus relatórios", font=title_font)
            label.pack(pady=20)

            self.frameTelaProduto = ctk.CTkFrame(master=telaCadastroProduto)
            self.frameTelaProduto.pack(pady=20, padx=40, fill='both', expand=True)
            
            
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
        username = bd.fetchone()

        bd.execute(buscaSenha, (self.user_entry.get(),))
        password = bd.fetchone()

        # fecha comunicação com banco
        bd.close()

        # testando credenciais
        if username and password and self.user_pass.get() == password[0]:
            # Oculta a janela de login
            app.withdraw()
            Produto(app)
        elif username and self.user_pass.get() != password[0]:
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
            sql = """INSERT INTO public."Usuario"("Nome", "Email", "Senha", "CNPJ", "DadosBancario") VALUES(%s, %s, %s,%s,%s)"""
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

            self.botaoCadastro = ctk.CTkButton(master=self.frameCadastro,text='Cadastrar', width=250, font=placeholder_botao, command=self.enviaDadosUsuarios)
            self.botaoCadastro.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")


if __name__ == "__main__":
    Usuario(app)

#inicia aplicação tkinter
app.mainloop()
telaCadastro.mainloop()
telaCadastroProduto.mainloop()