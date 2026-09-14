import sqlite3

class GerenciadorBanco:
    _caminho_banco: str = "sistema_tarefas.db"

    @classmethod
    def definir_caminho(cls, novo_caminho: str) -> None:
        cls._caminho_banco = novo_caminho

    @classmethod
    def obter_conexao(cls) -> sqlite3.Connection:
        conexao = sqlite3.connect(cls._caminho_banco)
        conexao.row_factory = sqlite3.Row
        # habilita restricoes de chaves estrangeiras no sqlite
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

    @staticmethod
    def inicializar_tabelas() -> None:
        ddl = """
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            concluida INTEGER DEFAULT 0,
            projeto_id INTEGER NOT NULL,
            FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS etiquetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            cor TEXT DEFAULT 'cinza'
        );

        CREATE TABLE IF NOT EXISTS tarefas_etiquetas (
            tarefa_id INTEGER NOT NULL,
            etiqueta_id INTEGER NOT NULL,
            PRIMARY KEY (tarefa_id, etiqueta_id),
            FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE,
            FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id) ON DELETE CASCADE
        );
        """
        with GerenciadorBanco.obter_conexao() as conexao:
            conexao.executescript(ddl)
