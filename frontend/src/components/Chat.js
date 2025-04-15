import React, { useState } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [context, setContext] = useState(''); // Добавляем контекст

  const sendMessage = async () => {
    if (userInput.trim()) {
      const newMessages = [...messages, { text: userInput, from: 'user' }];
      setMessages(newMessages);
      
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userInput,
          context: context
        }),
      });
      const data = await response.json();
      setMessages([...newMessages, { text: data.answer, from: 'ai' }]);
      setUserInput('');
    }
  };

  return (
    <div>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={msg.from}>
            <p>{msg.text}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <textarea
        placeholder="Контекст"
        value={context}
        onChange={(e) => setContext(e.target.value)}
      />
      <button onClick={sendMessage}>Отправить</button>
    </div>
  );
};

export default Chat;
