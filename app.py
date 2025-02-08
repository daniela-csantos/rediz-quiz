from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)
r = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

def generate_id():
    return r.incr("id_counter")

@app.route('/quizzes', methods=['POST'])
def create_quiz():
    data = request.get_json()
    title = data.get('title')
    
    quiz_id = generate_id()
    
    r.hmset(f"quiz:{quiz_id}", {"title": title})
    
    return jsonify({"message": "Quiz criado com sucesso!", "quiz_id": quiz_id}), 201

@app.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
def create_question(quiz_id):
    data = request.get_json()
    question = data.get('question')
    alternatives = data.get('alternatives')
    
    if not question or not alternatives:
        return jsonify({"error": "Pergunta e alternativas são obrigatórias!"}), 400
    
    question_id = generate_id()
    
    r.hmset(f"quiz:{quiz_id}:question:{question_id}", {"question": question, "alternatives": json.dumps(alternatives)})
    
    return jsonify({"message": "Pergunta criada com sucesso!", "question_id": question_id}), 201

@app.route('/quizzes/<int:quiz_id>/questions/<int:question_id>/answers', methods=['POST'])
def register_answer(quiz_id, question_id):
    data = request.get_json()
    student_id = data.get('student_id')
    selected_alternative = data.get('selected_alternative')
    time_taken = data.get('time_taken')  
    
    if not student_id or not selected_alternative:
        return jsonify({"error": "Aluno e alternativa selecionada são obrigatórios!"}), 400
    
    r.hmset(f"quiz:{quiz_id}:question:{question_id}:answers", {f"student:{student_id}": selected_alternative})
    
    r.hincrby(f"quiz:{quiz_id}:question:{question_id}:votes", selected_alternative, 1)
    
    r.hset(f"quiz:{quiz_id}:question:{question_id}:response_times", f"student:{student_id}", time_taken)
    
    return jsonify({"message": "Resposta registrada com sucesso!"}), 200

@app.route('/quizzes/<int:quiz_id>/questions/<int:question_id>/rankings/alternatives', methods=['GET'])
def get_ranking_alternatives(quiz_id, question_id):
    votes = r.hgetall(f"quiz:{quiz_id}:question:{question_id}:votes")
    
    if not votes:
        return jsonify({"error": "Sem votos registrados para essa questão."}), 404
    
    sorted_votes = sorted(votes.items(), key=lambda x: int(x[1]), reverse=True)
    
    ranking = {alternative: int(votes) for alternative, votes in sorted_votes}
    
    return jsonify({"ranking": ranking})

@app.route('/quizzes/<int:quiz_id>/rankings/questions', methods=['GET'])
def get_ranking_questions(quiz_id):
    questions = r.keys(f"quiz:{quiz_id}:question:*")
    
    rankings = []
    
    for question in questions:
        question_id = question.split(":")[-1]
        
        votes = r.hgetall(f"quiz:{quiz_id}:question:{question_id}:votes")
        total_answers = sum(int(votes[alt]) for alt in votes) if votes else 0
        total_abstentions = len(r.hgetall(f"quiz:{quiz_id}:question:{question_id}:response_times")) - total_answers
        
        correct_answers = int(votes.get('C', 0))
        
        total_time = 0
        num_responses = 0
        
        for student_id in r.hkeys(f"quiz:{quiz_id}:question:{question_id}:response_times"):
            time_taken = r.hget(f"quiz:{quiz_id}:question:{question_id}:response_times", student_id)
            if time_taken is not None:
                total_time += float(time_taken)  # Apenas soma se o tempo for válido
                num_responses += 1
        
        avg_time = total_time / num_responses if num_responses else 0
        
        rankings.append({
            "question_id": question_id,
            "acertos": correct_answers,
            "abstencao": total_abstentions,
            "tempo_medio": avg_time
        })
    
    return jsonify({"rankings": rankings})


@app.route('/quizzes/<int:quiz_id>/rankings/students', methods=['GET'])
def get_student_ranking(quiz_id):
    students = {}
    
    for question_id in r.keys(f"quiz:{quiz_id}:question:*"):
        question_id = question_id.split(":")[-1]
        student_ids = r.hkeys(f"quiz:{quiz_id}:question:{question_id}:answers")
        
        for student_id in student_ids:
            student_id = student_id.split(":")[1]
            selected_alternative = r.hget(f"quiz:{quiz_id}:question:{question_id}:answers", f"student:{student_id}")
            
            if student_id not in students:
                students[student_id] = {"acertos": 0, "tempo_total": 0, "num_respostas": 0}
            
            if selected_alternative == 'C':  
                students[student_id]["acertos"] += 1
            
            time_taken = float(r.hget(f"quiz:{quiz_id}:question:{question_id}:response_times", f"student:{student_id}"))
            students[student_id]["tempo_total"] += time_taken
            students[student_id]["num_respostas"] += 1
    
    student_ranking = []
    for student_id, data in students.items():
        avg_time = data["tempo_total"] / data["num_respostas"] if data["num_respostas"] else 0
        student_ranking.append({
            "student_id": student_id,
            "acertos": data["acertos"],
            "tempo_medio": avg_time
        })
    
    student_ranking = sorted(student_ranking, key=lambda x: (-x['acertos'], x['tempo_medio']))
    
    return jsonify({"ranking": student_ranking})

@app.route('/')
def home():
    return "Bem-vindo ao sistema de quiz!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
