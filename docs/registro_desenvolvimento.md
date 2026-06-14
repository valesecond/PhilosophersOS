# Registro de Desenvolvimento — PhilosophersOS

**Projeto:** PhilosophersOS — Simulador de Deadlock e Concorrência  
**Disciplina:** Sistemas Operacionais  
**Período:** 10 dias (Trabalho Prático)

---

## 1. Etapas Realizadas

| Dia | Etapa | Status |
|-----|-------|--------|
| 1–2 | Estudo do problema e escolha da linguagem (Python) | ✓ Concluído |
| 2–3 | Pseudocódigo, fluxograma e identificação da região crítica | ✓ Concluído |
| 3–4 | Implementação dos estados e threads dos filósofos | ✓ Concluído |
| 4–5 | Implementação dos garfos com Lock e versão deadlock | ✓ Concluído |
| 5–6 | Entrega intermediária (código parcial + documentação inicial) | ✓ Concluído |
| 6–7 | Implementação da solução com semáforo garçom | ✓ Concluído |
| 7–8 | Interface CLI com Rich e dashboard em tempo real | ✓ Concluído |
| 8–9 | Monitor de deadlock, testes e configurações | ✓ Concluído |
| 9–10 | Documentação final, relatório e registro de IA | ✓ Concluído |

---

## 2. Divisão de Tarefas

| Integrante | Responsabilidade |
|------------|-----------------|
| Membro 1 | Arquitetura, filósofos, estados e threads |
| Membro 2 | Sincronização, garfos, deadlock e solução |
| Membro 3 | Interface Rich, dashboards e monitoramento |
| Membro 4 | Documentação, testes, relatório e defesa |

*Nota: Ajustar nomes reais dos integrantes antes da entrega.*

---

## 3. Dificuldades Encontradas

1. **Sincronização do cenário de deadlock** — Garantir que todos pegassem o garfo esquerdo simultaneamente exigiu uso de `threading.Barrier`.
2. **Detecção confiável de deadlock** — Implementamos heurística baseada em timeout + estado WAITING de todos os filósofos.
3. **Interface em tempo real** — Rich Live exige cuidado com refresh rate e thread safety.
4. **Configuração dinâmica** — Separar parâmetros em `config.json` para facilitar demonstração em sala.

---

## 4. Decisões Tomadas

| Decisão | Justificativa |
|---------|---------------|
| Python + threading | Simplicidade, legibilidade e suporte nativo a locks/semáforos |
| Semáforo garçom (limite N-1) | Estratégia clássica, fácil de explicar e demonstrar |
| Rich para CLI | Interface profissional sem complexidade de GUI |
| Barrier na versão deadlock | Maximiza probabilidade de deadlock para demonstração |
| config.json externo | Professora pode alterar parâmetros sem editar código |
| Monitor externo de deadlock | Separa detecção da lógica dos filósofos |

---

## 5. Testes Realizados

| Teste | Resultado |
|-------|-----------|
| Estados obrigatórios (5 estados) | ✓ Passou |
| Fork usa Lock corretamente | ✓ Passou |
| Mesa com N filósofos customizados | ✓ Passou |
| Solução completa sem deadlock | ✓ Passou |
| Simulação manual versão deadlock | ✓ Deadlock detectado |
| Simulação manual versão solução | ✓ 15 refeições (5×3 ciclos) |
| Alteração via config.json | ✓ Funcional |

Comando: `pytest tests/ -q`

---

## 6. Uso de Inteligência Artificial

**Ferramenta:** Cursor AI (Claude)  
**Uso declarado:** Sim — como apoio ao desenvolvimento

---

## 7. Prompts Utilizados

1. *"Explique as quatro condições de Coffman no contexto do Jantar dos Filósofos"*
2. *"Como implementar semáforo garçom em Python com threading?"*
3. *"Estrutura de projeto Python para simulador de deadlock com Rich CLI"*
4. *"Como detectar deadlock quando todos os filósofos estão em WAITING?"*
5. *"Gerar relatório técnico acadêmico sobre implementação do Jantar dos Filósofos"*
6. *"Melhorar CLI com Rich: painéis, tabelas, dashboard em tempo real estilo htop"*

---

## 8. O Que Foi Aceito, Rejeitado ou Modificado

| Sugestão da IA | Decisão | Motivo |
|----------------|---------|--------|
| Estrutura modular em `src/` | **Aceito** | Organização clara e escalável |
| Semáforo garçom como solução | **Aceito** | Alinhado ao enunciado e fácil de defender |
| Timeout para detecção de deadlock | **Aceito com ajuste** | Adicionamos verificação de estado WAITING |
| Solução com ordem invertida de garfos | **Rejeitado** | Preferimos garçom por clareza didática |
| GUI com Tkinter | **Rejeitado** | Rich CLI atende requisito de terminal |
| Hardcoded Semaphore(4) | **Modificado** | Usamos `config.waiter_limit` configurável |
| Código sem comentários de região crítica | **Modificado** | Bloco explícito adicionado conforme enunciado |

---

## 9. Validação das Respostas da IA

- Execução manual comparando versão deadlock vs solução  
- Testes automatizados com pytest  
- Revisão teórica com material da disciplina  
- Simulação com 3, 5 e 7 filósofos via configuração  

---

*Registro elaborado para transparência acadêmica — uso responsável de IA conforme orientações da disciplina.*
