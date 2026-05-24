from abc import ABC, abstractmethod
from datetime import datetime

# =====================================================================
# 1. CLASSES DE ENTIDADE (CLASSES BASE)
# =====================================================================

class Paciente:
    def __init__(self, id_paciente: int, nome: String, cpf: String):
        self.id = id_paciente
        self.nome = nome
        self.cpf = cpf

class Medico:
    def __init__(self, id_medico: int, nome: String, crm: String):
        self.id = id_medico
        self.nome = nome
        self.crm = crm


# =====================================================================
# 2. O PRODUTO (INTERFACE/CLASSE ABSTRATA E IMPLEMENTAÇÕES CONCRETAS)
# =====================================================================

class TesteHospitalar(ABC):
    """Classe Abstrata que define a estrutura de um Teste/Exame."""
    
    def __init__(self, id_teste: int, paciente: Paciente, medico: Medico):
        self.id = id_teste
        self.data_solicitacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.paciente = paciente
        self.medico = medico

    @abstractmethod
    def exibir_detalhes(self) -> str:
        """Método abstrato que cada exame concreto deve implementar."""
        pass


class ExameSangue(TesteHospitalar):
    """Produto Concreto 1"""
    
    def __init__(self, id_teste: int, paciente: Paciente, medico: Medico, tipo_contagem: str = "Hemograma Completo"):
        super().__init__(id_teste, paciente, medico)
        self.tipo_contagem = tipo_contagem

    def exibir_detalhes(self) -> str:
        return (f"[EXAME DE SANGUE #{self.id}]\n"
                f"Data: {self.data_solicitacao}\n"
                f"Médico Solicitante: Dr(a). {self.medico.nome} (CRM: {self.medico.crm})\n"
                f"Paciente: {self.paciente.nome} (CPF: {self.paciente.cpf})\n"
                f"Tipo de Contagem: {self.tipo_contagem}\n"
                f"{'-'*40}")


class ExameRaioX(TesteHospitalar):
    """Produto Concreto 2"""
    
    def __init__(self, id_teste: int, paciente: Paciente, medico: Medico, regiao_corpo: str = "Tórax"):
        super().__init__(id_teste, paciente, medico)
        self.regiao_corpo = regiao_corpo

    def exibir_detalhes(self) -> str:
        return (f"[EXAME DE RAIO-X #{self.id}]\n"
                f"Data: {self.data_solicitacao}\n"
                f"Médico Solicitante: Dr(a). {self.medico.nome} (CRM: {self.medico.crm})\n"
                f"Paciente: {self.paciente.nome} (CPF: {self.paciente.cpf})\n"
                f"Região do Corpo: {self.regiao_corpo}\n"
                f"{'-'*40}")


# =====================================================================
# 3. O CRIADOR (FÁBRICA - FACTORY METHOD)
# =====================================================================

class SolicitadorDeTeste(ABC):
    """Classe Criadora Abstrata."""
    
    def __init__(self):
        self._proximo_id = 1  # Simulador de ID autoincremento

    def registrar_teste(self, paciente: Paciente, medico: Medico, tipo: str, detalhe_especifico: str) -> TesteHospitalar:
        """
        Método principal do Criador. Ele não sabe qual exame exato está criando,
        ele apenas confia no Factory Method (_criar_teste).
        """
        # Chama o Factory Method
        teste = self._criar_teste(self._proximo_id, paciente, medico, tipo, detalhe_especifico)
        self._proximo_id += 1
        
        # Aqui poderiam existir outras lógicas de negócio do hospital (ex: salvar no banco, enviar e-mail)
        print(f"-> Sistema Hospitalar: Registrando nova solicitação no banco de dados...")
        return teste

    @abstractmethod
    def _criar_teste(self, id_teste: int, paciente: Paciente, medico: Medico, tipo: str, detalhe: str) -> TesteHospitalar:
        """O FACTORY METHOD ABSTRATO"""
        pass


class GerenciadorDeTestes(SolicitadorDeTeste):
    """Classe Criadora Concreta que decide qual objeto instanciar."""
    
    def _criar_teste(self, id_teste: int, paciente: Paciente, medico: Medico, tipo: str, detalhe: str) -> TesteHospitalar:
        tipo = tipo.lower()
        if tipo == "sangue":
            return ExameSangue(id_teste, paciente, medico, tipo_contagem=detalhe)
        elif tipo == "raio-x" or tipo == "raiox":
            return ExameRaioX(id_teste, paciente, medico, regiao_corpo=detalhe)
        else:
            raise ValueError(f"Tipo de teste '{tipo}' não é suportado por esta fábrica.")


# =====================================================================
# 4. Demonstração de Uso (Fluxo do Sistema)
# =====================================================================
if __name__ == "__main__":
    print("=== SISTEMA HOSPITALAR - REGISTRO DE TESTES ===\n")

    # 1. Instanciando os atores (Médicos e Pacientes)
    medico1 = Medico(id_medico=101, nome="Carlos Adrian", crm="DF-12345")
    paciente1 = Paciente(id_paciente=501, nome="Arthur Elias", cpf="000.111.222-33")
    paciente2 = Paciente(id_paciente=502, nome="Antônio Silva", cpf="444.555.666-77")

    # 2. Instanciando a nossa Fábrica (Gerenciador)
    fabrica_hospitalar = GerenciadorDeTestes()

    # 3. Dr. Carlos solicita um Exame de Sangue para o paciente Arthur
    pedido1 = fabrica_hospitalar.registrar_teste(
        paciente=paciente1, 
        medico=medico1, 
        tipo="sangue", 
        detalhe_especifico="Hemograma + Glicemia"
    )
    
    # 4. Dr. Carlos solicita um Raio-X para o paciente Antônio
    pedido2 = fabrica_hospitalar.registrar_teste(
        paciente=paciente2, 
        medico=medico1, 
        tipo="raio-x", 
        detalhe_especifico="Articulação do Joelho"
    )

    print("\n=== IMPRESSÃO DOS TESTES REGISTRADOS ===")
    print(pedido1.exibir_detalhes())
    print(pedido2.exibir_detalhes())