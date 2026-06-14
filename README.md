# PhilosophersOS

PhilosophersOS e um simulador profissional de monitoramento de concorrencia e deadlocks para a disciplina de Sistemas Operacionais. O projeto demonstra, com uma CLI moderna em Rich, como o Problema do Jantar dos Filosofos expõe concorrencia, threads, compartilhamento de recursos, regiao critica, exclusao mutua, deadlock, sincronizacao, semaforos e starvation.

## Visao Geral

O sistema oferece duas estrategias principais:

- Versao com deadlock, em que todos os filosofos pegam primeiro o garfo esquerdo e depois tentam o direito.
- Versao com solucao, em que um semaforo de garcom limita a disputa simultanea por recursos.

A interface exibe estado em tempo real, resumo de execucao e monitoramento visual para facilitar apresentacao em sala.

## Estrutura

```text
PhilosophersOS/
├── src/
│   ├── philosophers/
│   │   ├── philosopher.py
│   │   ├── states.py
│   │   └── table.py
│   ├── synchronization/
│   │   ├── forks.py
│   │   ├── deadlock_version.py
│   │   └── solution_version.py
│   ├── monitors/
│   │   ├── deadlock_monitor.py
│   │   ├── statistics_monitor.py
│   │   └── execution_monitor.py
│   ├── views/
│   │   ├── main_menu_view.py
│   │   ├── deadlock_view.py
│   │   ├── solution_view.py
│   │   ├── comparison_view.py
│   │   ├── configuration_view.py
│   │   └── about_view.py
│   └── utils/
│       ├── logger.py
│       ├── config.py
│       ├── constants.py
│       └── helpers.py
├── docs/
├── assets/
├── tests/
├── README.md
├── requirements.txt
├── config.json
└── main.py
```

## Como Executar

1. Criar e ativar o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Iniciar o sistema:

```bash
python main.py
```

## Tela Principal

O menu principal apresenta as opcoes:

1. Simular Deadlock
2. Simular Solucao (Semaphore Waiter)
3. Comparar Implementacoes
4. Configuracoes
5. Sobre o Projeto
0. Encerrar Sistema

## Monitoramento em Tempo Real

Durante a execucao, o sistema mostra:

- tempo de execucao
- quantidade de refeicoes
- quantidade de deadlocks detectados
- threads ativas
- estrategia utilizada
- tabela com estado de cada filosofo e recursos em uso

## Como a Solucao Evita Deadlock

A versao de solucao usa `threading.Semaphore(4)` como garcom. Isso reduz a quantidade de filosofos que entram simultaneamente na disputa por garfos. Com um participante fora da competicao, a espera circular nao se fecha completamente, o que evita o deadlock.

## Configuracoes

As configuracoes sao salvas em `config.json`, sem necessidade de alterar codigo.

E possivel ajustar:

- quantidade de filosofos
- tempo de pensamento
- tempo de alimentacao
- velocidade da simulacao
- quantidade de ciclos

## Sobre o Projeto

Projeto: PhilosophersOS

Versao: 1.0.0

Disciplina: Sistemas Operacionais

Conceitos demonstrados:

- Concorrencia
- Threads
- Regiao Critica
- Exclusao Mutua
- Deadlock
- Sincronizacao
- Semaforos

## Testes

```bash
pytest
```

## Observacao

Os arquivos dentro de `docs/` e `assets/` funcionam como organizacao para os materiais de apresentacao, diagramas e registros do projeto.
