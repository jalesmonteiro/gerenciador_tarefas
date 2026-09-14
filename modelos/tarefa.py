import sqlite3
from banco.conexao import GerenciadorBanco
from modelos.base import EntidadeBase
from modelos.etiqueta import Etiqueta

class Tarefa(EntidadeBase):
    def __init__(
        self,
        titulo: str,
        descricao: str = "",
        concluida: bool = False,
        projeto_id: int | None = None,
        id_registro: int | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(id_registro=id_registro, *args, **kwargs)
        self._titulo: str = ""
        self.titulo = titulo  # aciona setter
        self.descricao: str = descricao
        self.concluida: bool = concluida
        self.projeto_id: int | None = projeto_id
        self.etiquetas: list[Etiqueta] = []  # agregacao

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("o titulo da tarefa nao pode ser vazio.")
        self._titulo = valor.strip()

    def adicionar_etiqueta(self, etiqueta: Etiqueta) -> None:
        if etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)

    def salvar(self) -> None:
        if not self.projeto_id:
            raise ValueError("a tarefa precisa estar vinculada a um projeto valido.")

        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            if self.id is None:
                sql = "INSERT INTO tarefas (titulo, descricao, concluida, projeto_id) VALUES (?, ?, ?, ?)"
                cursor.execute(sql, (self.titulo, self.descricao, int(self.concluida), self.projeto_id))
                self.id = cursor.lastrowid
            else:
                sql = "UPDATE tarefas SET titulo = ?, descricao = ?, concluida = ?, projeto_id = ? WHERE id = ?"
                cursor.execute(sql, (self.titulo, self.descricao, int(self.concluida), self.projeto_id, self.id))

            # sincronizar etiquetas agregadas
            for item in self.etiquetas:
                if item.id is None:
                    item.salvar()
                cursor.execute(
                    "INSERT OR IGNORE INTO tarefas_etiquetas (tarefa_id, etiqueta_id) VALUES (?, ?)",
                    (self.id, item.id),
                )

    @classmethod
    def buscar_pendentes_por_projeto(cls, projeto_id: int) -> list["Tarefa"]:
        sql = "SELECT id, titulo, descricao, concluida, projeto_id FROM tarefas WHERE projeto_id = ? AND concluida = 0"
        tarefas = []
        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            linhas = cursor.execute(sql, (projeto_id,)).fetchall()
            for row in linhas:
                instancia = cls(
                    titulo=row["titulo"],
                    descricao=row["descricao"],
                    concluida=bool(row["concluida"]),
                    projeto_id=row["projeto_id"],
                    id_registro=row["id"],
                )
                tarefas.append(instancia)
        return tarefas

class TarefaUrgente(Tarefa):
    """Especialização que sobrescreve comportamento padrão."""

    def __init__(self, titulo: str, prazo_horas: int = 24, *args, **kwargs) -> None:
        super().__init__(titulo=f"[URGENTE] {titulo}", *args, **kwargs)
        self.prazo_horas: int = prazo_horas

    def salvar(self) -> None:
        super().salvar()
        etiqueta_urgente = Etiqueta(nome="urgente", cor="vermelho")
        etiqueta_urgente.salvar()
        self.adicionar_etiqueta(etiqueta_urgente)
        with GerenciadorBanco.obter_conexao() as conexao:
            conexao.execute(
                "INSERT OR IGNORE INTO tarefas_etiquetas (tarefa_id, etiqueta_id) VALUES (?, ?)",
                (self.id, etiqueta_urgente.id),
            )
