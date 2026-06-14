# Relatório Técnico — PhilosophersOS

**Disciplina:** Sistemas Operacionais  
**Tema:** Deadlocks e o Problema do Jantar dos Filósofos  
**Linguagem:** Python 3.10+  
**Versão:** 1.0.0

---

## 1. Introdução

Deadlock é uma condição em sistemas concorrentes na qual um conjunto de processos ou threads permanece bloqueado indefinidamente, aguardando recursos uns dos outros. Essa situação ocorre quando quatro condições de Coffman são satisfeitas simultaneamente: exclusão mútua, posse e espera, não preempção e espera circular.

O Problema do Jantar dos Filósofos, proposto por Edsger Dijkstra, é um clássico modelo didático de concorrência. Nesse cenário, cinco filósofos sentam-se ao redor de uma mesa circular, com um garfo entre cada par de filósofos adjacentes. Para comer, cada filósofo precisa de dois garfos — o da esquerda e o da direita. Quando não está comendo, o filósofo pensa. Se todos pegarem simultaneamente o garfo esquerdo e aguardarem o direito, forma-se um deadlock.

Este trabalho implementa uma simulação interativa desse problema, demonstrando tanto a ocorrência (ou risco) de deadlock quanto uma estratégia de prevenção baseada em semáforo.

---

## 2. Descrição da Implementação

### 2.1 Linguagem e Ambiente

O projeto foi desenvolvido em **Python**, utilizando a biblioteca padrão `threading` para concorrência e a biblioteca **Rich** para interface de terminal profissional.

### 2.2 Representação dos Filósofos

Cada filósofo é representado por uma **thread** (`threading.Thread`), implementada na classe `Philosopher` em `src/philosophers/philosopher.py`. Cada thread executa um ciclo contínuo:

1. **THINKING** — pensar por tempo aleatório  
2. **HUNGRY** — ficar com fome  
3. **WAITING** — tentar adquirir os garfos  
4. **EATING** — comer  
5. **RELEASING** — liberar os garfos  

### 2.3 Representação dos Garfos

Os garfos são **recursos compartilhados** protegidos por **Locks** (`threading.Lock`), implementados na classe `Fork` em `src/synchronization/forks.py`. Cada garfo possui exclusão mútua: apenas um filósofo pode segurá-lo por vez.

### 2.4 Mecanismos de Sincronização

| Mecanismo | Localização | Função |
|-----------|-------------|--------|
| `threading.Lock` | `Fork._lock` | Exclusão mútua por garfo |
| `threading.Lock` | `DiningTable.state_lock` | Proteção do estado compartilhado |
| `threading.Semaphore` | `solution_version.py` | Garçom — limita filósofos na região crítica |
| `threading.Barrier` | `DiningTable` | Sincronização de início e cenário de deadlock |
| `threading.Event` | `DiningTable.stop_event` | Sinalização de encerramento |

### 2.5 Região Crítica

A região crítica está identificada em `src/philosophers/philosopher.py`, no método `_enter_critical_region()`, onde ocorre a aquisição dos dois garfos:

```python
left_fork.acquire(self.philosopher_id)
right_fork.acquire(self.philosopher_id)
```

Neste trecho, múltiplas threads acessam recursos compartilhados simultaneamente, exigindo sincronização rigorosa.

---

## 3. Demonstração do Problema

### 3.1 Versão com Deadlock

Na versão vulnerável (`src/synchronization/deadlock_version.py`), todos os filósofos:

1. Pegam o garfo esquerdo simultaneamente (via `threading.Barrier`)
2. Tentam pegar o garfo direito
3. Ficam bloqueados indefinidamente

### 3.2 Condições de Coffman Presentes

| Condição | Onde aparece |
|----------|--------------|
| **Exclusão mútua** | Cada garfo (`Lock`) só pode ser usado por um filósofo |
| **Posse e espera** | Filósofo segura um garfo enquanto espera o outro |
| **Não preempção** | Garfo não é retirado à força; só é liberado voluntariamente |
| **Espera circular** | P0→F0→P1→F1→...→P4→F4→P0 (ciclo fechado) |

### 3.3 Detecção

Um monitor dedicado (`DeadlockMonitor`) detecta deadlock quando todos os filósofos estão em estado `WAITING` e nenhum progresso ocorre por mais de 3 segundos (configurável).

---

## 4. Estratégia de Solução

### 4.1 Técnica Escolhida

**Garçom com Semáforo** — `threading.Semaphore(4)` limita a no máximo 4 filósofos disputando garfos simultaneamente (para 5 filósofos).

### 4.2 Condição Quebrada

A estratégia quebra a **espera circular**: com no máximo N-1 filósofos na região crítica, sempre haverá pelo menos um garfo disponível para algum filósofo completar sua refeição e liberar recursos.

### 4.3 Fluxo da Solução

1. Filósofo fica com fome  
2. Solicita permissão ao garçom (`waiter.acquire()`)  
3. Adquire garfos e come  
4. Libera garfos e devolve permissão (`waiter.release()`)  

---

## 5. Resultados Observados

### 5.1 Versão Deadlock

| Métrica | Resultado típico |
|---------|-----------------|
| Refeições | 0–1 (antes do bloqueio) |
| Deadlocks | 1 (detectado) |
| Tempo até bloqueio | ~3s |
| Threads bloqueadas | 5/5 |

### 5.2 Versão Solução

| Métrica | Resultado típico |
|---------|-----------------|
| Refeições | 15 (5 filósofos × 3 ciclos) |
| Deadlocks | 0 |
| Execução | Completa sem bloqueio |
| Progresso | Contínuo |

### 5.3 Comparativo

A versão com solução completa todos os ciclos configurados, enquanto a versão vulnerável trava após deadlock. A interface Rich exibe tabelas, métricas e alertas em tempo real durante a execução.

---

## 6. Uso de Inteligência Artificial

### 6.1 Ferramenta Utilizada

**Cursor AI (Claude)** — assistente de programação integrado ao editor.

### 6.2 Finalidades

- Revisão de conceitos de deadlock e sincronização  
- Organização da arquitetura do projeto  
- Implementação da interface Rich  
- Geração de documentação e relatório  
- Identificação de melhorias na detecção de deadlock  

### 6.3 Sugestões Aproveitadas

- Estrutura modular (`src/philosophers`, `src/synchronization`, `src/ui`)  
- Dashboard em tempo real com Rich Live  
- Identificação explícita da região crítica no código  
- Semáforo garçom como estratégia de prevenção  

### 6.4 Alterações pelo Grupo

- Validação dos estados do filósofo  
- Configuração via `config.json`  
- Testes automatizados com pytest  
- Revisão dos comentários e documentação acadêmica  

### 6.5 Validação

- Execução manual das duas versões  
- Testes unitários (`pytest`)  
- Verificação dos 5 estados obrigatórios  
- Confirmação de deadlock na versão vulnerável e ausência na solução  

---

## 7. Conclusão

Este trabalho demonstrou na prática os conceitos fundamentais de concorrência e sincronização em Sistemas Operacionos. A implementação do Jantar dos Filósofos evidenciou como a disputa por recursos compartilhados pode levar a deadlock quando as quatro condições de Coffman são satisfeitas.

A solução com semáforo garçom provou ser eficaz ao limitar o número de filósofos na região crítica, quebrando a espera circular. O projeto também reforçou a importância de identificar regiões críticas, documentar mecanismos de sincronização e oferecer visualização clara do comportamento concorrente.

**Limitações:** A solução com garçom pode causar starvation em cenários específicos se não houver fairness no semáforo. O monitor de deadlock usa heurística de timeout, não detecção formal de ciclo no grafo de alocação.

---

*Relatório gerado para entrega acadêmica — PhilosophersOS v1.0.0*
