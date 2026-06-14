# Fluxograma — PhilosophersOS

## Fluxo Principal do Filósofo (Thread)

```text
                    ┌─────────────┐
                    │   INÍCIO    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Barrier   │  (sincroniza início)
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │      THINKING         │
              │   (pensar / dormir)   │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │       HUNGRY            │
              │    (ficar com fome)     │
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │  Solução?   │
                    └──┬───────┬──┘
                  Sim  │       │ Não
              ┌────────▼       │
              │ waiter.acquire │  (garçom)
              └────────┬───────┘
                       │
              ┌────────▼────────────────────────┐
              │ ═══ REGIÃO CRÍTICA ═══         │
              │ acquire(garfo_esquerdo)         │
              └────────┬────────────────────────┘
                       │
                ┌──────▼──────┐
                │  Deadlock?  │
                └──┬───────┬──┘
              Sim  │       │ Não
          ┌────────▼       │
          │ deadlock_      │  (Barrier: todos
          │ barrier.wait   │   pegam esquerdo)
          └────────┬───────┘
                   │
              ┌────▼────────────────────────┐
              │ acquire(garfo_direito)       │
              └────┬────────────────────────┘
                   │
              ┌────▼────────────┐
              │    EATING       │
              │   (comer)       │
              └────┬────────────┘
                   │
              ┌────▼────────────┐
              │   RELEASING     │
              │ release(garfos) │
              └────┬────────────┘
                   │
            ┌──────▼──────┐
            │  Solução?   │
            └──┬───────┬──┘
          Sim  │       │ Não
      ┌────────▼       │
      │ waiter.release │
      └────────┬───────┘
               │
        ┌──────▼──────┐
        │ Mais ciclos?│
        └──┬───────┬──┘
       Sim │       │ Não
           │       │
           │  ┌────▼────┐
           │  │   FIM   │
           │  └─────────┘
           │
           └──── (volta para THINKING)
```

---

## Fluxo do Monitor de Deadlock

```text
    ┌─────────────┐
    │   INÍCIO    │
    └──────┬──────┘
           │
    ┌──────▼──────────────┐
    │ sleep(poll_interval)│
    └──────┬──────────────┘
           │
    ┌──────▼──────────────────────┐
    │ Todos em WAITING?           │
    └──┬───────────────────────┬──┘
   Não │                       │ Sim
       │                ┌──────▼──────────────┐
       │                │ timeout excedido?   │
       │                └──┬───────────────┬──┘
       │               Não │               │ Sim
       │                   │        ┌──────▼──────────┐
       │                   │        │ alert_deadlock  │
       │                   │        │ stop_event.set  │
       │                   │        └──────┬──────────┘
       │                   │               │
       └───────────────────┴───────────────┘
                           │
                    (loop até stop)
```

---

## Diagrama de Recursos (5 Filósofos)

```text
              F4
           ╱      ╲
         P4        P0
         │   F0    │
         F3   ●   F1
         │  MESA  │
         P3   F2  P1
           ╲      ╱
              P2

P0 usa F0 (esq) + F1 (dir)
P1 usa F1 (esq) + F2 (dir)
P2 usa F2 (esq) + F3 (dir)
P3 usa F3 (esq) + F4 (dir)
P4 usa F4 (esq) + F0 (dir)  ← ciclo circular
```

---

## Pseudocódigo Resumido

```
PARA cada filósofo i (como thread):
    ENQUANTO ciclos > 0:
        estado ← THINKING
        dormir(tempo_pensamento)

        estado ← HUNGRY

        SE solução:
            waiter.acquire()

        // REGIÃO CRÍTICA
        estado ← WAITING
        garfo[i].lock.acquire()
        SE deadlock:
            barrier.wait()
        garfo[(i+1) % N].lock.acquire()

        estado ← EATING
        dormir(tempo_comer)

        estado ← RELEASING
        garfo[(i+1) % N].lock.release()
        garfo[i].lock.release()

        SE solução:
            waiter.release()
```

---

*Fluxograma do PhilosophersOS — referência para apresentação e defesa.*
