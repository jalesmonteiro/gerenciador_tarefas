from abc import ABC, abstractmethod

class EntidadeBase(ABC):
    total_entidades_criadas: int = 0  # atributo de classe

    def __init__(self, id_registro: int | None = None, *args, **kwargs) -> None:
        self.__id: int | None = id_registro  # atributo privado
        EntidadeBase.total_entidades_criadas += 1

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, novo_id: int) -> None:
        if not isinstance(novo_id, int) or novo_id <= 0:
            raise ValueError("o identificador deve ser um inteiro positivo.")
        self.__id = novo_id

    @abstractmethod
    def salvar(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.__id}>"
