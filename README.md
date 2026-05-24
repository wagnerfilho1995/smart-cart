# 🛒 Feira Inteligente

Aplicativo para auxiliar na tomada de decisão durante compras mensais, ajudando a comparar preços atuais com históricos, identificar melhores custos-benefícios e manter registro completo das feiras realizadas.

---

# 📖 Visão Geral

O objetivo deste projeto é desenvolver um aplicativo gratuito e simples que funcione como uma memória auxiliar durante compras em supermercados e atacados.

O sistema permitirá:

* Registrar produtos comprados
* Registrar feiras completas
* Consultar histórico de preços
* Comparar preços atuais com preços anteriores
* Comparar produtos com diferentes pesos/volumes
* Identificar melhores custos-benefícios
* Controlar gastos mensais

O foco principal é permitir decisões rápidas durante a compra.

---

# 🎯 Problema

Durante compras mensais é comum enfrentar dificuldades como:

* Não lembrar quanto um produto custava anteriormente
* Não saber se um preço atual está caro ou barato
* Dificuldade em comparar produtos com pesos/volumes diferentes
* Preços especiais de atacado confundirem o histórico
* Perda de controle sobre gastos totais

Exemplo:

Leite em pó:

* Produto A → R$13,00 / 300g
* Produto B → R$14,90 / 400g

Embora o Produto B seja mais caro, ele pode ter melhor custo-benefício.

---

# 🎯 Objetivos

## Objetivo principal

Permitir que o usuário registre e consulte rapidamente históricos de compra para tomar decisões mais inteligentes.

## Objetivos secundários

* Calcular preço médio
* Calcular preço por unidade
* Diferenciar preço normal e preço de atacado
* Controlar gastos por feira
* Analisar histórico de compras
* Auxiliar a memória do usuário

---

# 🚀 Funcionalidades

## Cadastro de Produtos

Cada produto poderá conter:

* Nome
* Marca (opcional)
* Categoria (opcional)

---

## Cadastro de Feira

Uma feira representa um evento completo de compra.

Cada feira deverá possuir:

* Data
* Supermercado
* Valor total
* Lista de itens comprados

---

## Registro de Itens

Cada item da feira deve conter:

* Produto
* Preço
* Quantidade
* Unidade de medida
* Quantidade comprada

Exemplo:

| Produto     | Preço   | Quantidade | Unidade |
| ----------- | ------- | ---------- | ------- |
| Leite em pó | R$13,00 | 300        | g       |

---

## Histórico de Preços

O sistema deverá mostrar:

* Último preço pago
* Menor preço
* Maior preço
* Preço médio
* Data
* Local da compra
* Tipo de preço

---

## Comparação de Produtos

Permitir comparação por unidade base:

Exemplo:

| Produto   | Valor   | Peso | Resultado  |
| --------- | ------- | ---- | ---------- |
| Produto A | R$13,00 | 300g | R$43,33/kg |
| Produto B | R$14,90 | 400g | R$37,25/kg |

Resultado:

Produto B possui melhor custo-benefício.

---

## Suporte a Atacado

Produtos podem possuir preços especiais.

Exemplo:

Preço normal:

* R$10,00 (1 unidade)

Preço atacado:

* R$8,50 (mínimo 12 unidades)

Esses valores devem ser tratados separadamente no histórico.

---

# 👤 Fluxo do Usuário

## 1. Criar feira

Usuário abre o aplicativo:

* Nova Feira
* Histórico de Feiras

---

## 2. Adicionar produtos

Durante a compra:

* Buscar produto
* Selecionar produto existente ou criar novo
* Inserir preço
* Inserir quantidade
* Inserir unidade
* Informar se é compra normal ou atacado

---

## 3. Consultar histórico

Usuário poderá pesquisar produtos:

Exemplo:

```text
molho de...
```

Sugestão automática:

```text
molho de tomate
```

Visualizar:

* Último preço
* Histórico
* Média
* Tendência

---

## 4. Comparar produtos

Usuário poderá adicionar múltiplos produtos para comparação:

Exemplo:

```text
Produto A → R$13 / 300g
Produto B → R$14,90 / 400g
```

Sistema calcula:

* Preço por unidade
* Melhor opção

---

## 5. Finalizar feira

Ao finalizar:

Sistema exibe:

* Total da feira
* Quantidade de itens
* Resumo

Usuário salva a compra.

---

# 🧠 Regras de Negócio

### RN01

Todos os preços devem ser normalizados para uma unidade base.

Exemplos:

* g → kg
* ml → litro

---

### RN02

Preço de atacado e preço normal devem ser armazenados separadamente.

---

### RN03

Comparações devem priorizar histórico do mesmo tipo.

Exemplo:

* Atacado → histórico de atacado
* Normal → histórico normal

---

### RN04

O sistema nunca deve misturar automaticamente histórico normal com histórico de atacado.

---

### RN05

O valor total da feira será calculado automaticamente pela soma dos itens.

---

# 📦 Estrutura Inicial

## Produto

```text
id
nome
marca
categoria
```

## Feira

```text
id
data
supermercado
valor_total
```

## ItemFeira

```text
id
feira_id
produto_id
preco_total
quantidade
unidade_medida
quantidade_comprada
tipo_preco
quantidade_minima_atacado
preco_unitario
```

---

# ✅ MVP

Primeira versão:

* Cadastro de produtos
* Cadastro de feira
* Adição de itens
* Histórico de preços
* Busca de produtos
* Comparação de preços
* Cálculo automático por unidade
* Suporte a atacado

---

# 🔮 Futuras melhorias

* Gráficos de variação
* Comparação entre supermercados
* Leitura de código de barras
* Backup em nuvem
* Compartilhamento
* Alertas de preço ideal

---

# 📌 Status

Em planejamento 🚧
