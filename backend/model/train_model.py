from transformers import BertForQuestionAnswering, Trainer, TrainingArguments
from datasets import Dataset
from transformers import BertTokenizer

# Загружаем модель и токенизатор
tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
model = BertForQuestionAnswering.from_pretrained('DeepPavlov/rubert-base-cased')

# Пример подготовленных данных, для теста
data = [
    {
        'context': "Технология процесса производства формалина включает в себя следующие основные стадии...",
        'question': "Какие стадии включает процесс производства формалина?",
        'answer': "Получение формальдегида каталитическим окислением метанола кислородом воздуха..."
    },
    {
        'context': "Очистка отходящих газов установки термокаталитическим окислением...",
        'question': "Что включает очистка отходящих газов?",
        'answer': "Очистка отходящих газов установки термокаталитическим окислением."
    }
]

# Преобразуем данные в формат HFD
dataset = Dataset.from_dict({
    'context': [entry['context'] for entry in data],
    'question': [entry['question'] for entry in data],
    'answer': [entry['answer'] for entry in data]
})

# Подготовка данных
def preprocess_function(examples):
    return tokenizer(examples['question'], examples['context'], truncation=True, padding=True)

dataset = dataset.map(preprocess_function, batched=True)

# Определяем параметры обучения
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    logging_dir='./logs',
)

# Тренируем модель
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

# Сохраняем модель после тренировки
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")
