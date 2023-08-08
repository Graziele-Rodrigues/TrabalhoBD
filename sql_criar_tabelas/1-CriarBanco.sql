CREATE TABLE "Usuario" (
  "Nome" varchar(255),
  "Email" varchar(255),
  "Senha" varchar(255),
  "CNPJ" char(14) PRIMARY KEY,
  "DadosBancario" varchar(255)
);

CREATE TABLE "GeneroMusical" (
  "GeneroMusical_PK" int PRIMARY KEY,
  "GeneroMusical" varchar(255)
);

CREATE TABLE "Produto" (
  "CodigoBarras" varchar(255) PRIMARY KEY,
  "Nome" varchar(255),
  "Capa" varchar(255),
  "Descricao" varchar(255),
  "Idioma" varchar(255),
  "DataLancamento" Date,
  "fk_Usuario_Cnpj" varchar(255),
  FOREIGN KEY ("fk_Usuario_Cnpj") REFERENCES "Usuario" ("CNPJ")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "Album" (
  "fk_Produto_CodigoBarras" varchar(255) PRIMARY KEY,
  CONSTRAINT "fk_Album_fk_Produto_CodigoBarras" FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "FaixaMusical_Single" (
  "ISRC" varchar(255) PRIMARY KEY,
  "Nome" varchar(255),
  "TempoDuracao" varchar(255),
  "fk_GeneroMusical_GeneroMusical_PK" int,
  "FaixaMusical" varchar(255),
  "fk_Album_fk_Produto_CodigoBarras" varchar(255) UNIQUE,
  "fk_Produto_CodigoBarras" varchar(255) UNIQUE,
  FOREIGN KEY ("fk_GeneroMusical_GeneroMusical_PK") REFERENCES "GeneroMusical" ("GeneroMusical_PK")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_Album_fk_Produto_CodigoBarras") REFERENCES "Album" ("fk_Produto_CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "Pessoa" (
  "RedeSocial" varchar(255),
  "Nome" varchar(255),
  "EmailContato" varchar(255),
  "CPF" char(11) PRIMARY KEY,
  "fk_Usuario_CNPJ" char(14),
  FOREIGN KEY ("fk_Usuario_CNPJ") REFERENCES "Usuario" ("CNPJ")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "Participa" (
  "idParticipa" int PRIMARY KEY,
  "fk_Pessoa_CPF" char(11),
  "fk_FaixaMusical_Single_ISRC" varchar(255),
  "fk_FaixaMusical_Single_fk_Produto_CodigoBarras" varchar(255),
  "TipoPessoa" varchar(255),
  FOREIGN KEY ("fk_Pessoa_CPF") REFERENCES "Pessoa" ("CPF")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_FaixaMusical_Single_ISRC") REFERENCES "FaixaMusical_Single" ("ISRC")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_FaixaMusical_Single_fk_Produto_CodigoBarras") REFERENCES "FaixaMusical_Single" ("fk_Produto_CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "PlataformaDigital" (
  "CNPJ" char(14) PRIMARY KEY,
  "Nome" varchar(255),
  "ValorPagoReproducao" float
);

CREATE TABLE "Distribuido" (
  "fk_PlataformaDigital_cnpj" char(14),
  "fk_Produto_CodigoBarras" varchar(255),
  PRIMARY KEY ("fk_PlataformaDigital_cnpj", "fk_Produto_CodigoBarras"),
  FOREIGN KEY ("fk_PlataformaDigital_cnpj") REFERENCES "PlataformaDigital" ("CNPJ")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE "Reproduzida" (
  "idReproduzida" int PRIMARY KEY,
  "fk_PlataformaDigital_cnpj" char(14),
  "fk_FaixaMusical_Single_ISRC" varchar(255),
  "fk_FaixaMusical_Single_fk_Produto_CodigoBarras" varchar(255),
  "DataReproducao" Date,
  "QuantidadeReproducao" int,
  FOREIGN KEY ("fk_PlataformaDigital_cnpj") REFERENCES "PlataformaDigital" ("CNPJ")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_FaixaMusical_Single_ISRC") REFERENCES "FaixaMusical_Single" ("ISRC")
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY ("fk_FaixaMusical_Single_fk_Produto_CodigoBarras") REFERENCES "FaixaMusical_Single" ("fk_Produto_CodigoBarras")
    ON DELETE SET NULL
    ON UPDATE CASCADE
);