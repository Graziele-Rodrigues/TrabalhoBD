CREATE TABLE "Usuario" (
  "Nome" varchar(255),
  "Email" varchar(255),
  "Senha" varchar(255),
  "CNPJ" char(14) PRIMARY KEY,
  "DadosBancario" varchar(255)
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
);

CREATE TABLE "Album" (
  "fk_Produto_CodigoBarras" varchar(255) PRIMARY KEY,
  CONSTRAINT "fk_Album_fk_Produto_CodigoBarras" FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
);

CREATE TABLE "GeneroMusical" (
  "GeneroMusical_PK" int PRIMARY KEY,
  "GeneroMusical" varchar(255)
);

CREATE TABLE "FaixaMusical_Single" (
  "ISRC" varchar(255) PRIMARY KEY,
  "Nome" varchar(255),
  "TempoDuracao" varchar(255),
  "fk_GeneroMusical_GeneroMusical_PK" int,
  "FaixaMusical" varchar(255),
  "fk_Album_fk_Produto_CodigoBarras" varchar(255) UNIQUE,
  "fk_Produto_CodigoBarras" varchar(255) UNIQUE,  -- Adiciona a restrição UNIQUE nesta coluna
  FOREIGN KEY ("fk_GeneroMusical_GeneroMusical_PK") REFERENCES "GeneroMusical" ("GeneroMusical_PK"),
  FOREIGN KEY ("fk_Album_fk_Produto_CodigoBarras") REFERENCES "Album" ("fk_Produto_CodigoBarras"),
  FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
);

CREATE TABLE "Pessoa" (
  "RedeSocial" varchar(255),
  "Nome" varchar(255),
  "EmailContato" varchar(255),
  "CPF" char(11) PRIMARY KEY,
  "fk_Usuario_CNPJ" char(14),
  FOREIGN KEY ("fk_Usuario_CNPJ") REFERENCES "Usuario" ("CNPJ")
);

CREATE TABLE "Participa" (
  "idParticipa" int PRIMARY KEY,
  "fk_Pessoa_CPF" char(11),
  "fk_FaixaMusical_Single_ISRC" varchar(255),
  "fk_FaixaMusical_Single_fk_Produto_CodigoBarras" varchar(255),
  "TipoPessoa" varchar(255),
  FOREIGN KEY ("fk_Pessoa_CPF") REFERENCES "Pessoa" ("CPF"),
  FOREIGN KEY ("fk_FaixaMusical_Single_ISRC") REFERENCES "FaixaMusical_Single" ("ISRC"),
  FOREIGN KEY ("fk_FaixaMusical_Single_fk_Produto_CodigoBarras") REFERENCES "FaixaMusical_Single" ("fk_Produto_CodigoBarras")
);

CREATE TABLE "PlataformaDigital" (
  "CNPJ" char(14) PRIMARY KEY,
  "Nome" varchar(255)
);

CREATE TABLE "Distribuido" (
  "fk_PlataformaDigital_cnpj" char(14),
  "fk_Produto_CodigoBarras" varchar(255),
  PRIMARY KEY ("fk_PlataformaDigital_cnpj", "fk_Produto_CodigoBarras"),
  FOREIGN KEY ("fk_PlataformaDigital_cnpj") REFERENCES "PlataformaDigital" ("CNPJ"),
  FOREIGN KEY ("fk_Produto_CodigoBarras") REFERENCES "Produto" ("CodigoBarras")
);

CREATE TABLE "Reproduzida" (
  "idReproduzida" int PRIMARY KEY,
  "fk_PlataformaDigital_cnpj" char(14),
  "fk_FaixaMusical_Single_ISRC" varchar(255),
  "fk_FaixaMusical_Single_fk_Produto_CodigoBarras" varchar(255),
  "DataReproducao" Date,
  "QuantidadeReproducao" int,
  FOREIGN KEY ("fk_PlataformaDigital_cnpj") REFERENCES "PlataformaDigital" ("CNPJ"),
  FOREIGN KEY ("fk_FaixaMusical_Single_ISRC") REFERENCES "FaixaMusical_Single" ("ISRC"),
  FOREIGN KEY ("fk_FaixaMusical_Single_fk_Produto_CodigoBarras") REFERENCES "FaixaMusical_Single" ("fk_Produto_CodigoBarras")
);

INSERT INTO "PlataformaDigital" ("CNPJ", "Nome") VALUES
  ('11111111111111', 'Spotify'),
  ('22222222222222', 'Apple Music'),
  ('33333333333333', 'Deezer'),
  ('44444444444444', 'Amazon Music'),
  ('55555555555555', 'YouTube Music');
 
 INSERT INTO "PlataformaDigital" ("CNPJ", "Nome") VALUES
  ('66666666666666', 'Tidal'),
  ('77777777777777', 'SoundCloud'),
  ('88888888888888', 'Pandora'),
  ('99999999999999', 'Google Play Music');

  
 
 INSERT INTO "GeneroMusical" ("GeneroMusical_PK", "GeneroMusical") VALUES
  (1, 'Pop'),
  (2, 'Rock'),
  (3, 'Hip Hop'),
  (4, 'Eletrônica'),
  (5, 'Sertanejo');

 INSERT INTO "GeneroMusical" ("GeneroMusical_PK", "GeneroMusical") VALUES
  (6, 'R&B'),
  (7, 'Indie'),
  (8, 'Reggae'),
  (9, 'Funk'),
  (10, 'Country');

  INSERT INTO "GeneroMusical" ("GeneroMusical_PK", "GeneroMusical") VALUES
  (16, 'Pop Rock'),
  (17, 'Rap'),
  (18, 'Electronic Dance Music'),
  (19, 'Country Pop'),
  (20, 'Reggaeton');

