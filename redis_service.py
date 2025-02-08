import json
from config import get_redis_client
# TTL padrão em segundos (30 dias)
TTL_PADRAO = 30 * 24 * 60 * 60  # 30 dias em segundos

def create_quiz(quiz_id, title):
    redis_client = get_redis_client()

    redis_client.hset(f"quiz:{quiz_id}", "title", title)
    redis_client.expire(f"quiz:{quiz_id}",TTL_PADRAO)
    return {"status": "Quiz created successfully!"}

def add_question(quiz_id, question_id, question_data):
    redis_client = get_redis_client()

    redis_client.set(f"quiz:{quiz_id}:question:{question_id}", json.dumps(question_data))
    redis_client.expire(f"quiz:{quiz_id}:question:{question_id}",TTL_PADRAO)

    return {"status": "Question added successfully!"}

def get_quiz(quiz_id):
    redis_client = get_redis_client()

    title = redis_client.hget(f"quiz:{quiz_id}", "title")
    
    return {"quiz_id": quiz_id, "title": title}

def get_question(quiz_id, question_id):
    redis_client = get_redis_client()

    question_data = redis_client.get(f"quiz:{quiz_id}:question:{question_id}")
    
    if question_data:
        return {"question": json.loads(question_data)}
    else:
        return {"error": "Question not found."}

def update_question(quiz_id, question_id, updated_data):
    redis_client = get_redis_client()

    redis_client.set(f"quiz:{quiz_id}:question:{question_id}", json.dumps(updated_data))
    redis_client.expire(f"quiz:{quiz_id}:question:{question_id}",TTL_PADRAO)

    return {"status": "Question updated successfully!"}

def delete_question(quiz_id, question_id):
    redis_client = get_redis_client()

    redis_client.delete(f"quiz:{quiz_id}:question:{question_id}")
    
    return {"status": "Question deleted successfully!"}
