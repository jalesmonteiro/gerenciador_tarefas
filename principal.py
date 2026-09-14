from banco.conexao import GerenciadorBanco
from modelos.base import EntidadeBase
from modelos.etiqueta import Etiqueta
from modelos.projeto import Projeto
from modelos.tarefa import Tarefa

def executar() -> None:
    # 1. inicializacao
    GerenciadorBanco.inicializar_tabelas()

    try:
        # 2. criacao e persistencia do projeto
        projeto_web = Projeto(titulo="Refatoracao do Portal Academico", descricao="Migracao para nova infraestrutura")
        projeto_web.salvar()
        print(f"projeto persistido: {projeto_web.titulo} (ID={projeto_web.id})")

        # 3. composicao: criacao de tarefas diretamente pelo projeto
        t1 = projeto_web.criar_tarefa(titulo="Mapear tabelas antigas", descricao="Levantamento do schema atual")
        t2 = projeto_web.criar_tarefa(titulo="Falha de autenticacao", urgente=True, prazo_horas=12)

        # 4. agregacao: criacao independente de etiqueta e associacao a tarefa
        tag_banco = Etiqueta(nome="banco de dados", cor="verde")
        tag_banco.salvar()
        t1.adicionar_etiqueta(tag_banco)
        t1.salvar()

        # 5. consulta centralizada na entidade
        print("\n--- buscando tarefas pendentes via metodo de dominio ---")
        pendentes = Tarefa.buscar_pendentes_por_projeto(projeto_web.id)
        for tarefa in pendentes:
            print(f"- [ID={tarefa.id}] {tarefa.titulo} | Concluida: {tarefa.concluida}")

        # 6. teste de validacao do setter e tratamento de excecao
        print("\n--- validando encapsulamento e excecoes ---")
        t1.titulo = ""  # lanca ValueError

    except ValueError as erro:
        print(f"excecao capturada com sucesso: {erro}")

    finally:
        print(f"\ntotal de instancias criadas durante a execucao: {EntidadeBase.total_entidades_criadas}")

if __name__ == "__main__":
    executar()
