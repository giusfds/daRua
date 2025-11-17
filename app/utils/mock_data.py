"""
Módulo de Dados Mockados para o Sistema Somos DaRua
Este arquivo contém funções que retornam dados fictícios para simular
a operação do sistema sem conexão com banco de dados.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# ============================================================================
# DOADORES MOCKADOS
# ============================================================================

def get_doadores_mockados():
    """Retorna lista de 30 doadores fictícios"""
    nomes = [
        "João Silva", "Maria Santos", "Pedro Oliveira", "Ana Costa",
        "Carlos Souza", "Juliana Almeida", "Ricardo Ferreira", "Fernanda Lima",
        "Paulo Rodrigues", "Mariana Carvalho", "Lucas Martins", "Patrícia Ribeiro",
        "Roberto Gomes", "Camila Araújo", "Felipe Barbosa", "Amanda Dias",
        "Gustavo Cardoso", "Beatriz Cavalcanti", "Rafael Monteiro", "Larissa Teixeira",
        "Thiago Nascimento", "Vanessa Rocha", "Diego Pinto", "Gabriela Correia",
        "Bruno Vieira", "Isabela Mendes", "André Freitas", "Carolina Castro",
        "Marcelo Azevedo", "Renata Pires"
    ]
    
    doadores = []
    for i, nome in enumerate(nomes, 1):
        primeiro_nome = nome.split()[0].lower()
        sobrenome = nome.split()[1].lower()
        doadores.append({
            "id": i,
            "nome": nome,
            "cpf": f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}",
            "email": f"{primeiro_nome}.{sobrenome}@email.com",
            "telefone": f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            "endereco": f"Rua {random.choice(['das Flores', 'dos Pinheiros', 'Augusta', 'Consolação', 'Paulista', 'Vergueiro'])}, {random.randint(100,9999)} - São Paulo, SP",
            "data_cadastro": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d")
        })
    
    return doadores


# ============================================================================
# BENEFICIÁRIOS MOCKADOS
# ============================================================================

def get_beneficiarios_mockados():
    """Retorna lista de 40 beneficiários fictícios"""
    nomes = [
        "José da Silva", "Maria das Graças", "Antônio Pereira", "Francisca Souza",
        "Paulo Roberto", "Rita de Cássia", "João Paulo", "Conceição Santos",
        "Manoel Costa", "Aparecida Lima", "Sebastião Oliveira", "Terezinha Alves",
        "Francisco José", "Luzia Maria", "Raimundo Nonato", "Socorro Rodrigues",
        "Geraldo Ferreira", "Benedita Cruz", "Joaquim Barbosa", "Ivone Nascimento",
        "Valdemar Gomes", "Zilda Martins", "Osvaldo Araújo", "Edna Cardoso",
        "Nilton Silva", "Marlene Dias", "Waldemar Santos", "Neuza Ribeiro",
        "Ademar Costa", "Elza Monteiro", "Milton Carvalho", "Dalva Teixeira",
        "Benedito Rocha", "Célia Pinto", "Durval Mendes", "Dirce Correia",
        "Laércio Vieira", "Nair Freitas", "Expedito Castro", "Zenaide Azevedo"
    ]
    
    generos = ["Masculino", "Feminino", "Masculino", "Feminino"] * 10
    descricoes = [
        "Pessoa em situação de rua há 2 anos",
        "Família desabrigada após enchente",
        "Idoso sem renda fixa",
        "Mãe solo com 3 filhos",
        "Desempregado após pandemia",
        "Refugiado venezuelano",
        "Portador de deficiência física",
        "Ex-dependente químico em recuperação"
    ]
    
    status_list = ["Ativo", "Ativo", "Ativo", "Inativo", "Aguardando"]
    necessidades_opcoes = ["Alimentação", "Vestuário", "Abrigo", "Saúde", "Educação"]
    
    beneficiarios = []
    for i, (nome, genero) in enumerate(zip(nomes, generos), 1):
        idade = random.randint(8, 80)
        beneficiarios.append({
            "id": i,
            "nome": nome,
            "idade": idade,
            "genero": genero,
            "descricao": random.choice(descricoes),
            "necessidades": ", ".join(random.sample(necessidades_opcoes, random.randint(2, 4))),
            "status": random.choice(status_list),
            "data_cadastro": (datetime.now() - timedelta(days=random.randint(10, 500))).strftime("%Y-%m-%d")
        })
    
    return beneficiarios


# ============================================================================
# DOAÇÕES MOCKADAS
# ============================================================================

def get_doacoes_mockadas():
    """Retorna lista de 120+ doações fictícias"""
    doadores = get_doadores_mockados()
    pontos = get_pontos_coleta_mockados()
    
    tipos = ["Alimentos", "Roupas", "Medicamentos", "Dinheiro", "Outros"]
    itens_por_tipo = {
        "Alimentos": ["Arroz", "Feijão", "Óleo", "Macarrão", "Açúcar", "Café", "Leite", "Cesta Básica"],
        "Roupas": ["Calças", "Camisetas", "Casacos", "Sapatos", "Meias", "Roupas de Cama"],
        "Medicamentos": ["Analgésicos", "Antibióticos", "Anti-inflamatórios", "Vitaminas"],
        "Dinheiro": ["Doação em Dinheiro"],
        "Outros": ["Produtos de Limpeza", "Produtos de Higiene", "Brinquedos", "Livros"]
    }
    
    unidades_por_tipo = {
        "Alimentos": ["Kg", "Litros", "Unidades", "Caixas"],
        "Roupas": ["Unidades", "Sacas"],
        "Medicamentos": ["Caixas", "Unidades"],
        "Dinheiro": ["R$"],
        "Outros": ["Unidades", "Caixas"]
    }
    
    status_list = ["Recebida", "Recebida", "Recebida", "Em Triagem", "Distribuída"]
    
    doacoes = []
    for i in range(1, 121):
        tipo = random.choice(tipos)
        item = random.choice(itens_por_tipo[tipo])
        unidade = random.choice(unidades_por_tipo[tipo])
        
        if unidade == "R$":
            quantidade = random.randint(50, 5000)
        elif unidade == "Kg":
            quantidade = random.randint(5, 100)
        else:
            quantidade = random.randint(1, 50)
        
        doacoes.append({
            "id": i,
            "data": (datetime.now() - timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
            "doador": random.choice(doadores)["nome"],
            "tipo": tipo,
            "item": item,
            "quantidade": quantidade,
            "unidade": unidade,
            "ponto_coleta": random.choice(pontos)["nome"],
            "status": random.choice(status_list),
            "observacoes": random.choice(["", "", "Doação urgente", "Entregar até fim do mês", ""])
        })
    
    return doacoes


# ============================================================================
# CAMPANHAS MOCKADAS
# ============================================================================

def get_campanhas_mockadas():
    """Retorna lista de 12 campanhas fictícias"""
    campanhas = [
        {
            "id": 1,
            "nome": "Natal Solidário 2024",
            "descricao": "Campanha de arrecadação de alimentos e brinquedos para o Natal. Meta: beneficiar 500 famílias.",
            "data_inicio": "2024-11-01",
            "data_fim": "2024-12-20",
            "meta": 50000,
            "arrecadado": 42000,
            "tipo_meta": "R$",
            "tipos_doacao": "Alimentos, Brinquedos, Dinheiro",
            "responsavel": "Maria Santos",
            "status": "Ativa"
        },
        {
            "id": 2,
            "nome": "Campanha do Agasalho 2024",
            "descricao": "Arrecadação de roupas de inverno, cobertores e agasalhos para pessoas em situação de rua.",
            "data_inicio": "2024-05-01",
            "data_fim": "2024-08-31",
            "meta": 2000,
            "arrecadado": 2000,
            "tipo_meta": "Peças",
            "tipos_doacao": "Roupas",
            "responsavel": "Carlos Souza",
            "status": "Concluída"
        },
        {
            "id": 3,
            "nome": "Volta às Aulas Solidária",
            "descricao": "Arrecadação de material escolar para crianças carentes. Meta: 300 kits completos.",
            "data_inicio": "2024-12-01",
            "data_fim": "2025-02-15",
            "meta": 300,
            "arrecadado": 85,
            "tipo_meta": "Kits",
            "tipos_doacao": "Material Escolar",
            "responsavel": "Juliana Almeida",
            "status": "Ativa"
        },
        {
            "id": 4,
            "nome": "Saúde para Todos",
            "descricao": "Campanha de arrecadação de medicamentos e produtos de higiene pessoal.",
            "data_inicio": "2024-10-01",
            "data_fim": "2024-12-31",
            "meta": 30000,
            "arrecadado": 22500,
            "tipo_meta": "R$",
            "tipos_doacao": "Medicamentos, Higiene",
            "responsavel": "Ricardo Ferreira",
            "status": "Ativa"
        },
        {
            "id": 5,
            "nome": "Páscoa Solidária 2024",
            "descricao": "Distribuição de ovos de páscoa e cestas básicas para famílias carentes.",
            "data_inicio": "2024-03-01",
            "data_fim": "2024-04-07",
            "meta": 1000,
            "arrecadado": 1000,
            "tipo_meta": "Cestas",
            "tipos_doacao": "Alimentos, Doces",
            "responsavel": "Fernanda Lima",
            "status": "Concluída"
        },
        {
            "id": 6,
            "nome": "Lar Seguro - Reforma de Abrigos",
            "descricao": "Arrecadação de fundos para reforma e manutenção de abrigos temporários.",
            "data_inicio": "2024-09-01",
            "data_fim": "2025-03-31",
            "meta": 100000,
            "arrecadado": 35000,
            "tipo_meta": "R$",
            "tipos_doacao": "Dinheiro",
            "responsavel": "Paulo Rodrigues",
            "status": "Ativa"
        },
        {
            "id": 7,
            "nome": "Alimentação Digna",
            "descricao": "Campanha permanente de arrecadação de alimentos não perecíveis.",
            "data_inicio": "2024-01-01",
            "data_fim": "2024-12-31",
            "meta": 10000,
            "arrecadado": 7500,
            "tipo_meta": "Kg",
            "tipos_doacao": "Alimentos",
            "responsavel": "Mariana Carvalho",
            "status": "Ativa"
        },
        {
            "id": 8,
            "nome": "Dia das Crianças Feliz",
            "descricao": "Arrecadação de brinquedos e jogos para crianças em vulnerabilidade.",
            "data_inicio": "2024-09-01",
            "data_fim": "2024-10-12",
            "meta": 500,
            "arrecadado": 500,
            "tipo_meta": "Brinquedos",
            "tipos_doacao": "Brinquedos",
            "responsavel": "Lucas Martins",
            "status": "Concluída"
        },
        {
            "id": 9,
            "nome": "Projeto Dignidade",
            "descricao": "Distribuição de kits de higiene pessoal para pessoas em situação de rua.",
            "data_inicio": "2024-11-01",
            "data_fim": "2025-01-31",
            "meta": 1000,
            "arrecadado": 450,
            "tipo_meta": "Kits",
            "tipos_doacao": "Higiene",
            "responsavel": "Patrícia Ribeiro",
            "status": "Ativa"
        },
        {
            "id": 10,
            "nome": "Sopão Solidário",
            "descricao": "Arrecadação de alimentos para preparo de refeições diárias para 200 pessoas.",
            "data_inicio": "2024-06-01",
            "data_fim": "2024-12-31",
            "meta": 25000,
            "arrecadado": 18750,
            "tipo_meta": "R$",
            "tipos_doacao": "Alimentos, Dinheiro",
            "responsavel": "Roberto Gomes",
            "status": "Ativa"
        },
        {
            "id": 11,
            "nome": "Livros que Transformam",
            "descricao": "Campanha de arrecadação de livros e materiais de leitura para alfabetização de adultos.",
            "data_inicio": "2024-08-01",
            "data_fim": "2024-11-30",
            "meta": 300,
            "arrecadado": 225,
            "tipo_meta": "Livros",
            "tipos_doacao": "Livros",
            "responsavel": "Camila Araújo",
            "status": "Ativa"
        },
        {
            "id": 12,
            "nome": "Inverno Quentinho",
            "descricao": "Distribuição de cobertores e kits de proteção contra o frio.",
            "data_inicio": "2024-06-01",
            "data_fim": "2024-08-31",
            "meta": 800,
            "arrecadado": 800,
            "tipo_meta": "Kits",
            "tipos_doacao": "Cobertores, Roupas",
            "responsavel": "Felipe Barbosa",
            "status": "Concluída"
        }
    ]
    
    return campanhas


# ============================================================================
# PONTOS DE COLETA MOCKADOS
# ============================================================================

def get_pontos_coleta_mockados():
    """Retorna lista de 15 pontos de coleta fictícios"""
    pontos = [
        {
            "id": 1,
            "nome": "Centro Comunitário da Mooca",
            "endereco": "Rua da Mooca, 456 - Mooca, São Paulo, SP - CEP: 03104-000",
            "horario": "Seg-Sex 8h-18h",
            "responsavel": "Ana Paula Silva",
            "telefone": "(11) 3456-7890",
            "email": "mooca@somosdarua.org",
            "status": "Ativo"
        },
        {
            "id": 2,
            "nome": "Igreja Nossa Senhora Aparecida",
            "endereco": "Av. Paulista, 1234 - Bela Vista, São Paulo, SP - CEP: 01310-100",
            "horario": "Ter-Sáb 9h-17h",
            "responsavel": "Padre José Carlos",
            "telefone": "(11) 3287-1234",
            "email": "igreja.nsa@somosdarua.org",
            "status": "Ativo"
        },
        {
            "id": 3,
            "nome": "ONG Vida Nova - Sede Centro",
            "endereco": "Rua Barão de Itapetininga, 89 - República, São Paulo, SP - CEP: 01042-000",
            "horario": "Seg-Sex 9h-19h, Sáb 9h-13h",
            "responsavel": "Marcos Antonio Souza",
            "telefone": "(11) 3259-8765",
            "email": "centro@vidanova.org.br",
            "status": "Ativo"
        },
        {
            "id": 4,
            "nome": "Paróquia São Judas Tadeu",
            "endereco": "Rua Jabaquara, 2000 - Saúde, São Paulo, SP - CEP: 04045-000",
            "horario": "Todos os dias 7h-20h",
            "responsavel": "Irmã Maria de Lourdes",
            "telefone": "(11) 5571-3456",
            "email": "paroquia.sjt@somosdarua.org",
            "status": "Ativo"
        },
        {
            "id": 5,
            "nome": "Associação Amigos do Bem",
            "endereco": "Rua Augusta, 567 - Consolação, São Paulo, SP - CEP: 01305-000",
            "horario": "Seg-Sex 10h-18h",
            "responsavel": "Carla Mendes",
            "telefone": "(11) 3251-9876",
            "email": "contato@amigosbem.org.br",
            "status": "Ativo"
        },
        {
            "id": 6,
            "nome": "Centro de Referência Brasilândia",
            "endereco": "Av. Deputado Cantídio Sampaio, 2001 - Brasilândia, São Paulo, SP - CEP: 02802-000",
            "horario": "Seg-Sex 8h-17h",
            "responsavel": "Roberto Lima",
            "telefone": "(11) 3981-2345",
            "email": "brasilandia@prefeitura.sp.gov.br",
            "status": "Ativo"
        },
        {
            "id": 7,
            "nome": "Instituto Solidariedade Zona Leste",
            "endereco": "Rua Itaquera, 789 - Itaquera, São Paulo, SP - CEP: 08295-000",
            "horario": "Ter-Sáb 9h-16h",
            "responsavel": "Juliana Costa",
            "telefone": "(11) 2571-4567",
            "email": "zonaleste@institutosolidariedade.org",
            "status": "Ativo"
        },
        {
            "id": 8,
            "nome": "Templo Evangélico da Paz",
            "endereco": "Rua Vergueiro, 3456 - Vila Mariana, São Paulo, SP - CEP: 04101-000",
            "horario": "Seg-Dom 8h-20h",
            "responsavel": "Pastor Miguel Ferreira",
            "telefone": "(11) 5084-3210",
            "email": "templo.paz@somosdarua.org",
            "status": "Ativo"
        },
        {
            "id": 9,
            "nome": "Casa de Apoio Esperança",
            "endereco": "Rua dos Pinheiros, 890 - Pinheiros, São Paulo, SP - CEP: 05422-001",
            "horario": "Seg-Sex 9h-18h",
            "responsavel": "Fernanda Oliveira",
            "telefone": "(11) 3062-5678",
            "email": "esperanca@casadeapoio.org",
            "status": "Ativo"
        },
        {
            "id": 10,
            "nome": "Centro Social Capão Redondo",
            "endereco": "Estrada de Itapecerica, 4567 - Capão Redondo, São Paulo, SP - CEP: 05858-000",
            "horario": "Seg-Sex 7h-19h",
            "responsavel": "Paulo Henrique Santos",
            "telefone": "(11) 5822-9012",
            "email": "capaoredondo@centrosocial.org.br",
            "status": "Ativo"
        },
        {
            "id": 11,
            "nome": "ONG Mãos Unidas - Tatuapé",
            "endereco": "Rua Tuiuti, 1234 - Tatuapé, São Paulo, SP - CEP: 03081-000",
            "horario": "Seg-Sex 8h-17h, Sáb 8h-12h",
            "responsavel": "Sandra Regina",
            "telefone": "(11) 2097-3456",
            "email": "tatuape@maosunidas.org",
            "status": "Ativo"
        },
        {
            "id": 12,
            "nome": "Projeto Renascer - Santana",
            "endereco": "Av. Voluntários da Pátria, 2345 - Santana, São Paulo, SP - CEP: 02011-000",
            "horario": "Ter-Sáb 9h-18h",
            "responsavel": "Ricardo Alves",
            "telefone": "(11) 2950-6789",
            "email": "santana@renascer.org.br",
            "status": "Ativo"
        },
        {
            "id": 13,
            "nome": "Centro Franciscano de Assistência",
            "endereco": "Rua da Consolação, 1500 - Consolação, São Paulo, SP - CEP: 01302-001",
            "horario": "Todos os dias 6h-22h",
            "responsavel": "Frei Damião",
            "telefone": "(11) 3231-8901",
            "email": "franciscanos@somosdarua.org",
            "status": "Ativo"
        },
        {
            "id": 14,
            "nome": "Núcleo Comunitário Jardim Ângela",
            "endereco": "Estrada M'Boi Mirim, 5678 - Jardim Ângela, São Paulo, SP - CEP: 04948-000",
            "horario": "Seg-Sex 8h-16h",
            "responsavel": "Benedita Silva",
            "telefone": "(11) 5841-2345",
            "email": "jardimangela@nucleocomunitario.org",
            "status": "Ativo"
        },
        {
            "id": 15,
            "nome": "Associação Vida Plena - Penha",
            "endereco": "Rua Padre Adelino, 987 - Penha, São Paulo, SP - CEP: 03303-000",
            "horario": "Seg-Sex 9h-17h",
            "responsavel": "Adriana Martins",
            "telefone": "(11) 2095-4567",
            "email": "penha@vidaplena.org.br",
            "status": "Ativo"
        }
    ]
    
    return pontos


# ============================================================================
# VOLUNTÁRIOS MOCKADOS
# ============================================================================

def get_voluntarios_mockados():
    """Retorna lista de 30 voluntários fictícios"""
    nomes = [
        "Alexandre Pereira", "Bianca Rocha", "Caio Mendes", "Daniela Freitas",
        "Eduardo Castro", "Flávia Azevedo", "Gabriel Pires", "Helena Cardoso",
        "Igor Monteiro", "Jéssica Teixeira", "Kevin Nascimento", "Luana Correia",
        "Matheus Vieira", "Natália Dias", "Otávio Barbosa", "Priscila Cavalcanti",
        "Quintino Gomes", "Raquel Araújo", "Samuel Rodrigues", "Tatiana Almeida",
        "Ulisses Ferreira", "Valéria Lima", "William Carvalho", "Xuxa Martins",
        "Yuri Ribeiro", "Zélia Santos", "Arthur Costa", "Brenda Souza",
        "César Oliveira", "Diana Silva"
    ]
    
    areas = ["Logística", "Triagem", "Atendimento", "Administração", "TI"]
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    periodos = ["Manhã", "Tarde", "Noite", "Integral"]
    status_list = ["Ativo", "Ativo", "Ativo", "Inativo", "Aguardando aprovação"]
    
    voluntarios = []
    for i, nome in enumerate(nomes, 1):
        primeiro_nome = nome.split()[0].lower()
        sobrenome = nome.split()[1].lower()
        
        areas_selecionadas = random.sample(areas, random.randint(1, 3))
        disponibilidade = ", ".join(random.sample(dias_semana, random.randint(2, 5)))
        
        voluntarios.append({
            "id": i,
            "nome": nome,
            "cpf": f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}",
            "email": f"{primeiro_nome}.{sobrenome}@email.com",
            "telefone": f"(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            "data_nascimento": f"{random.randint(1960,2000)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "areas_atuacao": ", ".join(areas_selecionadas),
            "disponibilidade": disponibilidade,
            "periodo": random.choice(periodos),
            "experiencia": random.choice([
                "Já trabalhei em ONGs de assistência social",
                "Primeira experiência como voluntário",
                "Experiência com logística e distribuição",
                "Formação em Serviço Social",
                "Trabalhei em eventos solidários"
            ]),
            "status": random.choice(status_list),
            "data_cadastro": (datetime.now() - timedelta(days=random.randint(10, 365))).strftime("%Y-%m-%d")
        })
    
    return voluntarios


# ============================================================================
# MÉTRICAS DASHBOARD
# ============================================================================

def get_metricas_dashboard():
    """Retorna dicionário com métricas agregadas para o dashboard"""
    
    # Dados para gráfico de pizza - Doações por categoria
    doacoes_por_categoria = {
        "Alimentos": 450,
        "Roupas": 320,
        "Medicamentos": 180,
        "Outros": 150
    }
    
    # Dados para gráfico de barras - Doações mensais
    doacoes_mensais = {
        "Jan": 1200,
        "Fev": 1350,
        "Mar": 1100,
        "Abr": 1450,
        "Mai": 1600,
        "Jun": 1800
    }
    
    # Dados para gráfico de linha - Tendência de doadores
    doadores_mensais = {
        "Jan": 150,
        "Fev": 180,
        "Mar": 210,
        "Abr": 250,
        "Mai": 290,
        "Jun": 320
    }
    
    # Últimas doações
    ultimas_doacoes = get_doacoes_mockadas()[:10]
    
    return {
        "total_doadores": 1234,
        "total_beneficiarios": 567,
        "total_doacoes": 8900,
        "campanhas_ativas": 15,
        "doacoes_por_categoria": doacoes_por_categoria,
        "doacoes_mensais": doacoes_mensais,
        "doadores_mensais": doadores_mensais,
        "ultimas_doacoes": ultimas_doacoes
    }


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def get_df_doadores():
    """Retorna DataFrame do pandas com doadores"""
    return pd.DataFrame(get_doadores_mockados())

def get_df_beneficiarios():
    """Retorna DataFrame do pandas com beneficiários"""
    return pd.DataFrame(get_beneficiarios_mockados())

def get_df_doacoes():
    """Retorna DataFrame do pandas com doações"""
    return pd.DataFrame(get_doacoes_mockadas())

def get_df_campanhas():
    """Retorna DataFrame do pandas com campanhas"""
    return pd.DataFrame(get_campanhas_mockadas())

def get_df_pontos_coleta():
    """Retorna DataFrame do pandas com pontos de coleta"""
    return pd.DataFrame(get_pontos_coleta_mockados())

def get_df_voluntarios():
    """Retorna DataFrame do pandas com voluntários"""
    return pd.DataFrame(get_voluntarios_mockados())
