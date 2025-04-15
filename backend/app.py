from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForQuestionAnswering
from transformers import pipeline

app = Flask(__name__)

# Загружаем токенизатор и модель RuBERT для вопросов и ответов
tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
model = BertForQuestionAnswering.from_pretrained('DeepPavlov/rubert-base-cased')

# Создаем пайплайн для QA
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

@app.route('/chat', methods=['POST'])
def chat():
    # Извлекаем данные из запроса
    user_input = request.json['question']
    context = request.json['context']
    
    # Используем пайплайн для получения ответа
    answer = qa_pipeline({
        'context': context,
        'question': user_input
    })
    
    # Возвращаем ответ
    return jsonify({"answer": answer['answer']})

if __name__ == "__main__":
    app.run(debug=True)
