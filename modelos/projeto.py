from banco.conexao import GerenciadorBanco
from modelos.base import EntidadeBase
from modelos.tarefa import Tarefa, TarefaUrgente

class Projeto(EntidadeBase):
    def __init__(self, titulo, descricao = "", id_registro = None):
        super().__init__(id_registro=id_registro)
        self.titulo = titulo
        self.descricao = descricao
        self._tarefas = []  # composicao: gerenciadas pelo projeto

    def criar_tarefa(self, titulo, descricao = "", urgente = False):
        if self.id is None:
            raise ValueError("salve o projeto antes de associar tarefas a ele.")

        if urgente:
            tarefa = TarefaUrgente(titulo=titulo, descricao=descricao, projeto_id=self.id)
        else:
            tarefa = Tarefa(titulo=titulo, descricao=descricao, projeto_id=self.id)

        tarefa.salvar()
        self._tarefas.append(tarefa)
        return tarefa

    def salvar(self):
        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            if self.id is None:
                sql = "INSERT INTO projetos (titulo, descricao) VALUES (?, ?)"
                cursor.execute(sql, (self.titulo, self.descricao))
                self.id = cursor.lastrowid
            else:
                sql = "UPDATE projetos SET titulo = ?, descricao = ? WHERE id = ?"
                cursor.execute(sql, (self.titulo, self.descricao, self.id))

    @classmethod
    def carregar_com_tarefas(cls, id_projeto):
        with GerenciadorBanco.obter_conexao() as conexao:
            cursor = conexao.cursor()
            linha = cursor.execute("SELECT id, titulo, descricao FROM projetos WHERE id = ?", (id_projeto,)).fetchone()
            if not linha:
                return None

            projeto = cls(titulo=linha["titulo"], descricao=linha["descricao"], id_registro=linha["id"])
            projeto._tarefas = Tarefa.buscar_pendentes_por_projeto(projeto.id)
            return projeto
