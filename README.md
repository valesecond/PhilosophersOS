# PhilosophersOS

PhilosophersOS e um projeto didatico em Python para a disciplina de Sistemas Operacionais. Ele simula o Problema do Jantar dos Filosofos e mostra, de forma visual e modular, conceitos como concorrencia, threads, recursos compartilhados, regiao critica, exclusao mutua, deadlock, sincronizacao, semaforos e mutex/locks.

## Problema

No problema classico, varios filosofos estao sentados em torno de uma mesa circular. Entre cada par de filosofos existe um garfo. Para comer, cada filosofo precisa pegar os dois garfos ao lado. Isso cria um cenario perfeito para estudar concorrencia e seus riscos.

Se todos pegarem primeiro o garfo esquerdo e depois tentarem pegar o direito, um deadlock pode acontecer. PhilosophersOS demonstra exatamente esse comportamento e tambem apresenta uma solucao usando um semaforo como garcom.

## Conceitos de Sistemas Operacionais

- Concorrencia: varios filosofos executam ao mesmo tempo.
- Threads: cada filosofo roda em uma `threading.Thread`.
- Recursos compartilhados: os garfos sao compartilhados entre vizinhos.
- Regiao critica: o trecho em que um filosofo tenta pegar e usar os garfos.
- Exclusao mutua: cada garfo usa `threading.Lock`.
- Deadlock: a versao propositalmente insegura pode travar.
- Sincronizacao: o inicio dos filosofos e coordenado para evidenciar o problema.
- Semaforos: a solucao usa `threading.Semaphore` como garcom.
- Mutex/Locks: os garfos sao protegidos por locks.

## Estrutura do Projeto

```text
PhilosophersOS/
├── README.md
├── requirements.txt
├── main.py
├── philosophers/
│   ├── philosopher.py
│   ├── states.py
│   └── table.py
├── synchronization/
│   ├── forks.py
│   ├── deadlock_version.py
│   ├── solution_version.py
│   └── deadlock_monitor.py
├── utils/
│   ├── logger.py
│   ├── colors.py
│   └── config.py
└── tests/
    └── simulation_test.py
```

## Como Executar

### 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Executar o projeto

```bash
python main.py
```

## Menu Principal

Ao executar, voce vera um menu com as opcoes:

1. Executar versao com Deadlock
2. Executar versao com Solucao
3. Sair

## Como a Solucao Funciona

Na versao com solucao, um semaforo age como garcom e permite que apenas 4 filosofos tentem comer ao mesmo tempo. Como sempre sobra pelo menos um filosofo de fora da disputa, o ciclo circular de espera nao se fecha completamente e o deadlock e evitado.

## Como Alterar a Quantidade de Filosofos

Basta editar o arquivo [utils/config.py](utils/config.py) e alterar:

```python
NUM_PHILOSOPHERS = 5
```

Todos os modulos usam essa configuracao por padrao.

## Testes

```bash
pytest
```

## Observacoes

- A versao com deadlock foi criada de forma intencional para demonstrar o problema.
- As mensagens no terminal mostram claramente as transicoes de estado de cada filosofo.
- O codigo foi organizado de maneira modular e orientada a objetos para facilitar apresentacao em sala.
