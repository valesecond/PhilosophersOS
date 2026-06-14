# PhilosophersOS

<div align="center">

**Deadlock & Concurrency Simulator**

Simulador profissional do Problema do Jantar dos Filósofos para a disciplina de Sistemas Operacionais.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Rich](https://img.shields.io/badge/Rich-13.7+-magenta.svg)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

</div>

---

## Visão Geral

O **PhilosophersOS** é um simulador de laboratório que demonstra, na prática, os conceitos de:

- Concorrência e threads
- Recursos compartilhados e exclusão mútua
- Região crítica
- Deadlock e suas quatro condições (Coffman)
- Sincronização com Locks e Semáforos
- Prevenção de deadlock

A interface utiliza **Rich** para oferecer dashboards em tempo real, painéis, tabelas e monitoramento visual — no estilo de ferramentas como `htop` e `btop`.

---

## Demonstração Rápida

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

### Menu Principal

```
╔══════════════════════════════════════════════════════════════╗
║                     PHILOSOPHERS OS                         ║
║             Deadlock & Concurrency Simulator               ║
╚══════════════════════════════════════════════════════════════╝

  [1]  Simular Deadlock
  [2]  Simular Solução
  [3]  Comparar Implementações
  [4]  Configurações
  [5]  Arquitetura do Sistema
  [6]  Sobre
  [0]  Encerrar Sistema
```

---

## Estratégias Implementadas

| Versão | Estratégia | Resultado |
|--------|-----------|-----------|
| **Deadlock** | Todos pegam garfo esquerdo simultaneamente (Barrier) | Deadlock detectado |
| **Solução** | Garçom Semáforo — máx. N-1 filósofos na região crítica | Execução sem bloqueio |

### Por que a solução funciona?

O semáforo garçom (`threading.Semaphore`) limita quantos filósofos podem disputar garfos ao mesmo tempo. Com no máximo **N-1** participantes, a espera circular nunca se fecha completamente — sempre há progresso.

---

## Estrutura do Projeto

```text
PhilosophersOS/
├── src/
│   ├── philosophers/       # Threads, estados, mesa
│   │   ├── philosopher.py  # Filósofo (thread) + região crítica
│   │   ├── states.py       # THINKING, HUNGRY, WAITING, EATING, RELEASING
│   │   └── table.py        # Coordenação e estado compartilhado
│   ├── synchronization/    # Garfos, versões deadlock/solução
│   │   ├── forks.py        # Garfos com threading.Lock
│   │   ├── deadlock_version.py
│   │   └── solution_version.py
│   ├── monitors/           # Dashboard, deadlock, estatísticas
│   ├── views/              # Telas da CLI
│   ├── ui/                 # Componentes Rich (painéis, tabelas, cards)
│   └── utils/              # Config, logger, constantes
├── docs/
│   ├── relatorio.md              # Relatório técnico (entrega)
│   ├── registro_desenvolvimento.md
│   ├── arquitetura.md
│   ├── perguntas_defesa.md
│   └── fluxograma.md
├── tests/
├── config.json             # Configuração editável
├── main.py
└── requirements.txt
```

---

## Requisitos Atendidos

| Requisito | Status |
|-----------|--------|
| Filósofos como threads | ✓ |
| Garfos como Locks | ✓ |
| 5 estados (THINKING, HUNGRY, WAITING, EATING, RELEASING) | ✓ |
| Versão com risco de deadlock | ✓ |
| Versão com solução | ✓ |
| Demonstração clara da execução | ✓ |
| Comentários explicativos | ✓ |
| Região crítica identificada | ✓ |
| Mecanismos de sincronização identificados | ✓ |
| README completo | ✓ |
| Relatório técnico | ✓ (`docs/relatorio.md`) |
| Registro de desenvolvimento e IA | ✓ (`docs/registro_desenvolvimento.md`) |

---

## Configuração

Edite `config.json` sem alterar código:

```json
{
  "num_philosophers": 5,
  "thinking_time": 0.8,
  "eating_time": 0.6,
  "simulation_speed": 1.0,
  "cycles": 3,
  "deadlock_timeout": 3.0,
  "waiter_limit": 4
}
```

| Parâmetro | Descrição |
|-----------|-----------|
| `num_philosophers` | Quantidade de filósofos/threads |
| `thinking_time` | Tempo base de pensamento (s) |
| `eating_time` | Tempo base de alimentação (s) |
| `simulation_speed` | Multiplicador de velocidade |
| `cycles` | Ciclos por filósofo |
| `waiter_limit` | Limite do semáforo garçom |

---

## Dashboard em Tempo Real

Durante a execução, a interface mantém **dois painéis estáveis** (sem piscar a tela):

**Dashboard de Estado Atual**

```
P0 -> COMENDO
P1 -> ESPERANDO
P2 -> PENSANDO
```

**Log de Eventos** (histórico persistente — últimos 30 eventos)

```
[12:01:15] P0 começou a pensar
[12:01:18] P1 ficou com fome
[12:01:20] P1 começou a comer
```

- Atualização **somente por evento** (sem polling nem refresh constante)
- Log **não desaparece** — eventos permanecem visíveis no painel
- **Resumo final** fica na tela até pressionar Enter
- Alerta de deadlock integrado ao log com filósofos bloqueados e recursos

---

## Região Crítica

Identificada em `src/philosophers/philosopher.py`:

```python
# REGIÃO CRÍTICA — Acesso aos recursos compartilhados (garfos)
self.left_fork.acquire(self.philosopher_id)
self.right_fork.acquire(self.philosopher_id)
```

---

## Testes

```bash
pytest tests/ -q
```

---

## Documentação Acadêmica

| Documento | Conteúdo |
|-----------|----------|
| [`docs/relatorio.md`](docs/relatorio.md) | Relatório técnico completo |
| [`docs/registro_desenvolvimento.md`](docs/registro_desenvolvimento.md) | Etapas, IA, decisões |
| [`docs/arquitetura.md`](docs/arquitetura.md) | Arquitetura do sistema |
| [`docs/perguntas_defesa.md`](docs/perguntas_defesa.md) | Perguntas para defesa oral |
| [`docs/fluxograma.md`](docs/fluxograma.md) | Fluxogramas e pseudocódigo |

---

## Linguagem

**Python 3.10+** — escolhida por suporte nativo a `threading.Lock`, `threading.Semaphore`, `threading.Barrier` e legibilidade para demonstração em sala.

---

## Disciplina

**Sistemas Operacionais** — Trabalho Prático: Deadlocks e o Problema do Jantar dos Filósofos.

---

<div align="center">

*PhilosophersOS v1.0.0 — Desenvolvido para demonstração de concorrência e sincronização*

</div>
