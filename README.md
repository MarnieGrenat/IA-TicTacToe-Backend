
# 🧠 Board API – Documentação dos Endpoints

API responsável por controlar o estado de um tabuleiro (3x3) para aplicações como jogos da velha ou simulações de IA.

---

## 📍 Base URL

```
http://localhost:5000/
```

---

## 🔹 Endpoints

### `GET /board/v1/fetch`

**Descrição:**
Retorna o estado atual do tabuleiro.

**Parâmetros JSON opcionais:**

| Campo | Tipo  | Descrição                           |
|-------|-------|--------------------------------------|
| `raw` | bool  | Se `true`, retorna o estado numérico (interno). Se `false` ou ausente, retorna símbolos (`O` / `Y`). |

**Exemplo de corpo da requisição:**

```json
{
  "raw": false
}
```

**Resposta (raw = false):**

```json
{
  "message": "Presenting board",
  "board": [
    ["", "O", ""],
    ["", "", "Y"],
    ["", "", ""]
  ]
}
```

---

### `POST /board/v1/update`

**Descrição:**
Atualiza uma posição do tabuleiro com o símbolo desejado.

**Corpo JSON esperado:**

```json
{
  "s": -1,   // símbolo: -1 para "O", 1 para "Y"
  "x": 1,    // coordenada X (0 a 2)
  "y": 0     // coordenada Y (0 a 2)
}
```

**Resposta de sucesso:**

```json
{
  "message": "Board updated successfully"
}
```

**Resposta de erro:**

```json
{
  "message": "Failed to update board"
}
```

---

### `POST /board/v1/reset`

**Descrição:**
Reseta o tabuleiro para o estado inicial.

**Resposta:**

```json
{
  "message": "Board reset"
}
```

---

### `GET /board/v1/status`

**Descrição:**
Retorna um status simples confirmando que a classe `Board` foi coletada com sucesso.

**Resposta:**

```json
{
  "message": "Board class has been collected successfully"
}
```

---

## 🧪 Exemplos com `curl`

```bash
# Obter tabuleiro
curl -X GET http://localhost:5000/board/v1/fetch -H "Content-Type: application/json" -d '{"raw": false}'

# Atualizar uma célula
curl -X POST http://localhost:5000/board/v1/update \
     -H "Content-Type: application/json" \
     -d '{"s": 1, "x": 0, "y": 1}'

# Resetar o tabuleiro
curl -X POST http://localhost:5000/board/v1/reset

# Verificar status da instância
curl -X GET http://localhost:5000/board/v1/status
```

---

## 🛠️ Observações Técnicas

- `s`: deve ser `-1` (representa "O") ou `1` (representa "Y").
- `x` e `y`: valores inteiros entre `0` e `2`.
- Se a posição já estiver ocupada ou os dados forem inválidos, a atualização será rejeitada.
