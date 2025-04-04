
# 🧠 Board API – Documentação dos Endpoints

Esta API controla um objeto `Board` (tabuleiro 3x3), permitindo interações simples como atualização de células, visualização do estado atual e reset total.
---

## 📍 Base URL

```
http://localhost:5000/
```

---

## 🔹 Endpoints

### `GET /get`

**Descrição:**
Retorna o estado atual do tabuleiro, com os símbolos visuais.

**Resposta:**

```json
[
  ["", "O", ""],
  ["", "", "Y"],
  ["", "", ""]
]
```

---

### `POST /update`

**Descrição:**
Atualiza uma célula do tabuleiro com o símbolo `-1` (O) ou `1` (Y), na posição especificada.

**Body (JSON):**

```json
{
  "s": 1,    // símbolo: -1 para "O", 1 para "Y"
  "x": 0,    // coordenada X (0 a 2)
  "y": 1     // coordenada Y (0 a 2)
}
```

**Respostas possíveis:**

- `200 OK` – Atualização feita com sucesso.
- `400 Bad Request` – Dados ausentes ou inválidos.

**Resposta de sucesso:**

```json
{
  "message": "Board updated"
}
```

---

### `POST /reset`

**Descrição:**
Reseta o tabuleiro para o estado inicial (vazio).

**Resposta:**

```json
{
  "message": "Board reset"
}
```

---

### `GET /get_status`

**Descrição:**
Retorna o status geral da classe `Board`. Pode ser usado para verificar a integridade da instância.

**Resposta:**

```json
{
  "message": "Board class has been collected successfully"
}
```

---

## 🛠️ Observações Técnicas

- O símbolo `s` deve ser `1` (Y) ou `-1` (O). Outros valores serão ignorados.
- As coordenadas `x` e `y` devem estar no intervalo de `0` a `2`.
- O sistema **não bloqueia sobreposição de jogadas**. (podemos implementar no proximo commit)

---

## 🧪 Exemplos de uso via `curl`

```bash
# Ver tabuleiro atual
curl http://localhost:5000/get

# Atualizar o tabuleiro
curl -X POST http://localhost:5000/update \
     -H "Content-Type: application/json" \
     -d '{"s": 1, "x": 0, "y": 1}'

# Resetar o tabuleiro
curl -X POST http://localhost:5000/reset

# Verificar status da instância
curl http://localhost:5000/get_status
```