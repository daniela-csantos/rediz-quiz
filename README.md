# Quiz System - Flask + Redis

Integrantes do grupo:
1. Caio Chaves Guimarães – RM 353781
2. Daniela Cirino Santos – RM 355671
3. Yuri da Silva Mendes – RM 356197

Este projeto implementa um sistema de quiz online usando **Flask** para o backend e **Redis** como banco de dados. Professores podem criar quizzes, adicionar perguntas e alternativas, e os alunos podem responder as perguntas, com resultados sendo computados e exibidos em tempo real.

## Tecnologias Utilizadas

- **Python 3.9+**
- **Flask**: Framework web para criação de APIs RESTful.
- **Redis**: Banco de dados NoSQL usado para armazenar dados de quizzes, perguntas, respostas e rankings.
- **Postman**: Para testar a API de forma interativa e fácil.

## Funcionalidades

- **Cadastro de Quiz**: Professores podem criar novos quizzes.
- **Cadastro de Pergunta**: Adição de perguntas com alternativas de múltipla escolha.
- **Respostas dos Alunos**: Alunos podem responder às questões e registrar o tempo de resposta.
- **Ranking**:
  - Alternativas mais votadas.
  - Questões mais acertadas.
  - Questões com mais abstenções.
  - Tempo médio de resposta por questão.
  - Alunos com maior acerto e mais rápidos.
  - Alunos com maior acerto.
  - Alunos mais rápidos.

## Estrutura de Dados no Redis

O sistema usa diferentes estruturas de dados do Redis para armazenar informações:

- **Hash**: Armazenamento de dados como perguntas e alternativas.
- **Set**: Usado para armazenar alunos que responderam a uma determinada questão.
- **String**: Usado para armazenar o tempo de resposta de cada aluno.

### Exemplo de Estrutura:
- `quiz:{quiz_id}:question:{question_id}:votes`: Um hash para armazenar o número de votos de cada alternativa de uma pergunta.
- `quiz:{quiz_id}:question:{question_id}:response_times`: Um hash para armazenar os tempos de resposta dos alunos.
- `quiz:{quiz_id}:ranking:{ranking_type}`: Para armazenar rankings das alternativas mais votadas, questões mais acertadas, etc.

## Endpoints da API
Podem ser importados a partir do arquivo `API de Quiz - Flask + Redis.postman_collection.json`

Exemplo:

### 1. Criar Quiz
Cria um novo quiz.

**Método:** `POST`  
**Endpoint:** `/quizzes`

**Payload:**
```json
{
    "title": "Quiz de Matemática"
}
