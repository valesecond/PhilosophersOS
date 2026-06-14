# Perguntas para Defesa Oral — PhilosophersOS

Perguntas prováveis da professora com respostas preparadas para a apresentação.

---

## 1. O que é deadlock?

Deadlock é uma situação em que dois ou mais processos (ou threads) ficam bloqueados indefinidamente, cada um aguardando um recurso que está sendo mantido por outro participante do ciclo. Nenhum deles consegue prosseguir porque todos estão presos numa cadeia circular de espera.

No Jantar dos Filósofos, isso ocorre quando cada filósofo segura um garfo e espera pelo segundo — formando um ciclo fechado.

---

## 2. Onde aparece a exclusão mútua no problema?

A exclusão mútua aparece nos **garfos**. Cada garfo é um recurso que só pode ser usado por **um filósofo por vez**, garantido pelo `threading.Lock` na classe `Fork` (`src/synchronization/forks.py`).

```python
self._lock.acquire()  # Apenas um filósofo por garfo
```

---

## 3. Onde está a região crítica no código?

A região crítica está em `src/philosophers/philosopher.py`, método `_enter_critical_region()`:

```python
# REGIÃO CRÍTICA — Acesso aos recursos compartilhados (garfos)
self.left_fork.acquire(self.philosopher_id)
self.right_fork.acquire(self.philosopher_id)
```

É o trecho onde múltiplas threads acessam recursos compartilhados e podem causar condições de corrida ou deadlock.

---

## 4. Como os garfos foram representados?

Cada garfo é uma instância da classe `Fork`, contendo um `threading.Lock` que implementa exclusão mútua. O garfo F0 fica entre P0 e P1, F1 entre P1 e P2, e assim por diante, formando um arranjo circular.

---

## 5. Como os filósofos foram representados?

Cada filósofo é uma **thread** Python (`threading.Thread`), implementada na classe `Philosopher`. Cada thread executa independentemente o ciclo pensar → ficar com fome → pegar garfos → comer → liberar garfos.

---

## 6. Em que momento o filósofo tenta pegar o primeiro garfo?

No método `_enter_critical_region()`, após ficar com fome (estado HUNGRY). Primeiro adquire o **garfo esquerdo** (`self.left_fork.acquire()`), entrando no estado WAITING.

---

## 7. Em que momento ele tenta pegar o segundo garfo?

Imediatamente após obter o garfo esquerdo, ainda dentro da região crítica, o filósofo tenta adquirir o **garfo direito** (`self.right_fork.acquire()`).

---

## 8. Como o deadlock poderia acontecer nessa implementação?

Na versão vulnerável, um `threading.Barrier` sincroniza todos os filósofos para pegarem o garfo esquerdo **ao mesmo tempo**. Depois, cada um tenta o garfo direito — que está sendo segurado pelo vizinho. Como todos estão num ciclo de espera (P0 espera F1, P1 espera F2, ..., P4 espera F0), forma-se deadlock.

---

## 9. Qual estratégia foi usada para evitar o deadlock?

**Garçom com Semáforo** (`threading.Semaphore`). O semáforo limita a no máximo N-1 filósofos (4 para 5 filósofos) que podem tentar pegar garfos simultaneamente.

---

## 10. Por que essa estratégia funciona?

Porque **quebra a espera circular**. Com no máximo 4 de 5 filósofos disputando garfos, sempre existe pelo menos um filósofo que consegue obter ambos os garfos, comer e liberar recursos — permitindo que os demais prossigam.

---

## 11. Essa solução também evita starvation? Por quê?

**Parcialmente.** O semáforo padrão do Python não garante fairness (ordem FIFO estrita). Em teoria, um filósofo pode ser repetidamente preterido se outros sempre obtiverem o semáforo primeiro. Na prática, com tempos aleatórios de pensamento, a starvation é improvável mas **não impossível**.

Para garantir ausência de starvation, seria necessário um semáforo justo ou fila ordenada.

---

## 12. O que aconteceria se aumentássemos de 5 para 7 filósofos?

- **Versão deadlock:** Continuaria travando — o ciclo circular se forma com 7 filósofos e 7 garfos.
- **Versão solução:** O garçom limitaria a 6 filósofos simultâneos (`waiter_limit = N-1`). A lógica permanece válida; basta ajustar `num_philosophers` e `waiter_limit` no `config.json`.

---

## 13. O que aconteceria se removêssemos um mutex, lock ou semáforo?

| Remoção | Consequência |
|---------|-------------|
| Lock do garfo | Dois filósofos poderiam usar o mesmo garfo — corrida de dados |
| state_lock | Estado dos filósofos ficaria inconsistente na interface |
| Semáforo garçom | Volta o risco de deadlock na versão solução |
| stop_event | Simulação não encerraria corretamente após deadlock |

---

## 14. Qual parte do código foi mais difícil de implementar?

A **sincronização do cenário de deadlock** (Barrier + detecção confiável) e o **dashboard em tempo real** com Rich Live, que exige thread safety ao atualizar o estado compartilhado.

---

## 15. O que o grupo modificou depois dos testes?

- Semáforo passou de valor fixo (4) para configurável via `waiter_limit`
- Monitor de deadlock passou a registrar filósofos bloqueados e recursos aguardados
- Interface Rich foi expandida com painéis, cards e tela de arquitetura
- Comentários de região crítica e mecanismos de sincronização foram detalhados

---

## 16. A solução evita deadlock, starvation ou ambos?

- **Deadlock:** Sim, efetivamente evitado.
- **Starvation:** Não garantido formalmente — apenas reduzido na prática.

---

*Documento de preparação para defesa oral — revisar com o grupo antes da apresentação.*
