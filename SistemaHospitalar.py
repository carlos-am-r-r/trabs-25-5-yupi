from abc import ABC, abstractmethod
from datetime import datetime

# =====================================================================
# 1. CLASSES SIMPLES (Entidades fortes)
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
# 2. CLASSE ABSTRATA (ENTIDADE FRACA)
# =====================================================================

class TesteHospitalar(ABC):
    # Classe Abstrata que define a estrutura de um Teste/Exame
    
    def __init__(self, id_teste: int, paciente: Paciente, medico: Medico):
        self.id = id_teste
        self.data_solicitacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Configuração de datetime na instância
        self.paciente = paciente
        self.medico = medico

    @abstractmethod
    def exibir_detalhes(self) -> str:
        # Método abstrato para a implementação nas classes concretas
        # Obs: setinha declara o tipo de variável do método
        pass

# =====================================================================
# 2.1 CLASSES CONCRETAS
# =====================================================================

class ExameSangue(TesteHospitalar):
    # Classe concreta 1
    
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
    # Classe concreta 2
    
    def __init__(self, id_teste: int, paciente: Paciente, medico: Medico, regiao_corpo: str = "Tórax"):
        super().__init__(id_teste, paciente, medico)
        self.regiao_corpo = regiao_corpo

    # Método Get no contexto
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
    # Classe Criadora Abstrata
    
    def __init__(self):
        self._proximo_id = 1
        # Autoincremento de ID
        # Obs: o underline armazena o contador na classe em si

    def registrar_teste(self, paciente: Paciente, medico: Medico, tipo: str, detalhe_especifico: str) -> TesteHospitalar:
        # Método dependente do _criar_teste

        # Chama o Factory Method
        teste = self._criar_teste(self._proximo_id, paciente, medico, tipo, detalhe_especifico)
        self._proximo_id += 1
        
        # Mensagem de sucesso
        # Em caso de integrações, essa def mandaria pra um banco de dados
        print("-> Sistema Hospitalar: Registro bem sucedido")
        return teste

    @abstractmethod
    def _criar_teste(self, id_teste: int, paciente: Paciente, medico: Medico, tipo: str, detalhe: str) -> TesteHospitalar:
        # O FACTORY METHOD ABSTRATO
        pass


class GerenciadorDeTestes(SolicitadorDeTeste):
    # Classe Criadora Concreta que decide qual objeto instanciar
    # Obs: O JOHN FABRICA
    # Obs: o(≧∀≦)o
    
    def _criar_teste(self, id_teste: int, paciente: Paciente, medico: Medico, tipo: str, detalhe: str) -> TesteHospitalar:
        
        tipo = tipo.lower()
        if tipo == "sangue":
            return ExameSangue(id_teste, paciente, medico, tipo_contagem=detalhe)
        elif tipo == "raio-x" or tipo == "raiox":
            return ExameRaioX(id_teste, paciente, medico, regiao_corpo=detalhe)
        else:
            raise ValueError(f"Tipo de teste '{tipo}' não existe no sistema.")

# =====================================================================
# 3.1 Detalhamento Adicional (Ignorável)
# =====================================================================
"""
RASTREAMENTO DE CLASSES:

fabrica_hospitalar -> GerenciadorDeTestes -> SolicitadorDeTeste
$ Variável            $ Classe concreta      $ Classe abstrata

fabrica_hospitalar -> registrar_teste -> SolicitadorDeTeste
$ Variável            $ Método           $ Classe abstrata


tipo       -> ExameRaioX        -> TesteHospitalar
tipo       -> ExameSangue       -> TesteHospitalar
$ Atributo    $ Classe concreta    $ Classe abstrata

"""

# =====================================================================
# 4. Demonstração de Uso (Fluxo do Sistema)
# =====================================================================
if __name__ == "__main__":
    print("=== SISTEMA HOSPITALAR - REGISTRO DE TESTES ===\n")

    # 1. Instanciando os atores (Médicos e Pacientes)
    medico1 = Medico(id_medico=101, nome="Débora Abóbora", crm="DF-12345")
    paciente1 = Paciente(id_paciente=501, nome="Arthur Atum", cpf="000.111.222-33")
    paciente2 = Paciente(id_paciente=502, nome="Antônio Vinagres", cpf="444.555.666-77")
    # Obs: Repetição da variável para melhor visualização da classe

    # 2. Instanciando o Gerenciador (Fabrica)
    fabrica_hospitalar = GerenciadorDeTestes()

    # 3. Dr. Débora Abóbora solicita um Exame de Sangue para o paciente Arthur Atum
    pedido1 = fabrica_hospitalar.registrar_teste(
        paciente=paciente1, 
        medico=medico1, 
        tipo="sangue", 
        detalhe_especifico="Hemograma + Glicemia"
    )
    # Obs: professor voce gostou q eu usei o parenteses do python igual as chaves do java?
    # Obs: SS né
    
    # 4. Dr. Débora Abóbora solicita um Raio-X para o paciente Antônio Vinagres
    pedido2 = fabrica_hospitalar.registrar_teste(
        paciente=paciente2, 
        medico=medico1, 
        tipo="raio-x", 
        detalhe_especifico="Articulação do Joelho"
    )

    print("\n★ IMPRESSÃO DOS TESTES REGISTRADOS ★")
    print(pedido1.exibir_detalhes())
    print(pedido2.exibir_detalhes())
