import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
from itertools import cycle

fake = Faker('pt_BR')
np.random.seed(42)
random.seed(42)

# Definindo quantidades
num_clientes = 500
num_vendedores = 13
num_carros = 500
num_vendas = 500
num_fornecedores = 4

# Modelos 
modelos_bmw = [
    'Série 1', 'Série 2', 'Série 3', 'Série 4', 'Série 5', 
    'Série 7', 'Série 8', 'X1', 'X2', 'X3', 'X4', 'X5', 
    'X6', 'X7', 'Z4', 'i3', 'i4', 'i7', 'iX', 'iX3'
]

# Cores disponíveis
cores = ['Preto', 'Branco', 'Cinza', 'Prata', 'Azul', 'Vermelho', 'Verde']

#fabricas
fabricas = ['Regensburg - Alemanha', 'Araquari - Brasil', 'Munique - Alemanha', 'Leipzig - Alemanha']
fabrica_cycle = cycle(fabricas)

# Fornecedores 
fornecedores = pd.DataFrame({
    'id_fornecedor': range(1, num_fornecedores + 1),
    'fábrica': [next(fabrica_cycle) for _ in range(num_fornecedores)],
    'data_contrato': [fake.date_between(start_date='-5y', end_date='today') 
                      for _ in range(num_fornecedores)]
})

# Carros 
carros = pd.DataFrame({
    'id_carro': range(1, num_carros + 1),
    'modelo': [random.choice(modelos_bmw) for _ in range(num_carros)],
    'fabricacao': [random.choice(fabricas) for _ in range(num_carros)],
    'ano_fabricacao': [random.randint(2020, 2024) for _ in range(num_carros)],
    'cor': [random.choice(cores) for _ in range(num_carros)],
    'motor': [random.choice(['2.0 Turbo', '3.0 Turbo', 'Elétrico', 'Híbrido']) 
              for _ in range(num_carros)],
    'preco': [round(random.uniform(150000, 800000), 2) for _ in range(num_carros)],
    'quilometragem': [random.randint(0, 50000) for _ in range(num_carros)],
    'data_entrada_estoque': [fake.date_between(start_date='-1y', end_date='today') 
                             for _ in range(num_carros)]
})

# Vendedores 
vendedores = pd.DataFrame({
    'id_vendedor': range(1, num_vendedores + 1),
    'nome': [fake.name() for _ in range(num_vendedores)],
    'data_admissao': [fake.date_between(start_date='-5y', end_date='today') 
                      for _ in range(num_vendedores)],
    'comissao': [round(random.uniform(0.01, 0.03), 2) for _ in range(num_vendedores)]
})

# Clientes
clientes = pd.DataFrame({
    'id_cliente': range(1, num_clientes + 1),
    'nome': [fake.name() for _ in range(num_clientes)],
    'cpf': [fake.cpf() for _ in range(num_clientes)],
    'cidade': [fake.city() for _ in range(num_clientes)],
    'estado': [fake.estado_sigla() for _ in range(num_clientes)],
    'renda_anual': [round(random.uniform(50000, 500000), 2) for _ in range(num_clientes)]
})

# Vendas
vendas = pd.DataFrame({
    'id_venda': range(1, num_vendas + 1),
    'data_venda': [fake.date_between(start_date='-1y', end_date='today') 
                   for _ in range(num_vendas)],
    'id_cliente': [random.choice(clientes['id_cliente']) for _ in range(num_vendas)],
    'id_vendedor': [random.choice(vendedores['id_vendedor']) for _ in range(num_vendas)],
    'id_carro': [random.choice(carros['id_carro']) for _ in range(num_vendas)],
    'valor_venda': [0] * num_vendas,  # Será preenchido abaixo
    'forma_pagamento': [random.choice(['Financiamento', 'À vista', 'Consórcio']) 
                        for _ in range(num_vendas)],
    'taxa_juros': [0] * num_vendas  # Será preenchido abaixo
})

# Calculando valores de venda e taxas
for index, row in vendas.iterrows():
    carro = carros.loc[carros['id_carro'] == row['id_carro']].iloc[0]
    valor_base = carro['preco']
    
        
    # Ajuste pela forma de pagamento
    if row['forma_pagamento'] == 'À vista':
        valor_final = valor_base * random.uniform(0.95, 0.98)  # Desconto à vista
        taxa = 0
    elif row['forma_pagamento'] == 'Financiamento':
        valor_final = valor_base * random.uniform(1.0, 1.05)  # Acréscimo
        taxa = round(random.uniform(0.01, 0.03), 4)  # Taxa de juros anual
    else:  # Consórcio
        valor_final = valor_base
        taxa = round(random.uniform(0.005, 0.015), 4)
    
    vendas.at[index, 'valor_venda'] = round(valor_final, 2)
    vendas.at[index, 'taxa_juros'] = taxa

fornecedores.to_csv("fornecedores_bmw.csv", index=False)
carros.to_csv("carros_bmw.csv", index=False)
vendedores.to_csv("vendedores_bmw.csv", index=False)
clientes.to_csv("clientes_bmw.csv", index=False)
vendas.to_csv("vendas_bmw.csv", index=False)