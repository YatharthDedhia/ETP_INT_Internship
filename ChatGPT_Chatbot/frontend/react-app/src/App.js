import React, { useEffect, useState } from 'react';

const ChatApp = () => {
  const [inputValue, setInputValue] = useState('');
  const [receivedMessage, setReceivedMessage] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = new WebSocket('ws://localhost:8000/chat');

    newSocket.onopen = () => {
      console.log('WebSocket connection established');
    };

    newSocket.onmessage = (event) => {
      setReceivedMessage(event.data);
      console.log(receivedMessage)
    };

    newSocket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    setSocket(newSocket);

    return () => {
      if (newSocket) {
        newSocket.close();
      }
    };
  }, []);

  const sendMessage = (event) => {
    event.preventDefault();
    if (inputValue) {
      console.log(inputValue)
      socket.send(inputValue);
      setInputValue('');
    }
  };

  return (
    <div>
      <h1>ChatGPT Clone</h1>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
      <p>{receivedMessage}</p>

    </div>
  );
};

export default ChatApp;
