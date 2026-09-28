import sqlite3
from banco.conexao import GerenciadorBanco
from modelos.base import EntidadeBase

class Etiqueta(EntidadeBase):
    def __init__(self, nome, cor="azul", id_registro=None):
        super().__init__(id_registro=id_registro)
        self.nome = nome.strip().lower()
        self.cor = cor

    def salvar(self):
        sql = "INSERT OR IGNORE INTO etiquetas (nome, cor) VALUES (?, ?)"
        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(sql, (self.nome, self.cor))
            if cursor.lastrowid:
                self.id = cursor.lastrowid
            else:
                cursor.execute("SELECT id FROM etiquetas WHERE nome = ?", (self.nome,))
                self.id = cursor.fetchone()["id"]

    @classmethod
    def buscar_por_nome(cls, nome):
        sql = "SELECT id, nome, cor FROM etiquetas WHERE nome = ?"
        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            linha = cursor.execute(sql, (nome.strip().lower(),)).fetchone()
            if linha:
                return cls(nome=linha["nome"], cor=linha["cor"], id_registro=linha["id"])
            return None
