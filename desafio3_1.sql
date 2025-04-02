-- Tabela para operadoras ativas
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(100),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

-- Tabela para demonstrações contábeis
CREATE TABLE demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(20),
    competencia DATE,
    conta_contabil VARCHAR(100),
    descricao VARCHAR(255),
    valor DECIMAL(15,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- Índices para melhorar performance das consultas
CREATE INDEX idx_dc_registro_ans ON demonstracoes_contabeis(registro_ans);
CREATE INDEX idx_dc_competencia ON demonstracoes_contabeis(competencia);
CREATE INDEX idx_dc_conta_contabil ON demonstracoes_contabeis(conta_contabil);