"use client";

import React, { useState, useEffect } from 'react';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'Alice', text: 'Hello! How can I help you today?' },
    { id: 2, sender: 'User', text: 'Hi! I need some help with my order.' },
    { id: 3, sender: 'Alice', text: 'Sure, what seems to be the issue?' },
    { id: 4, sender: 'User', text: 'I received a wrong item in my order.' },
    { id: 5, sender: 'Alice', text: 'I apologize for the inconvenience. Can you please provide the order number?' },
    { id: 6, sender: 'User', text: 'Sure, it is #12345.' },
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    if (newMessage.length > 0) {
      setIsTyping(true);
    } else {
      setIsTyping(false);
    }
  }, [newMessage]);

  const handleSend = () => {
    if (newMessage.trim() !== '') {
      setMessages([...messages, { id: Date.now(), sender: 'User', text: newMessage }]);
      setNewMessage('');
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-500">
      <header className="bg-white shadow-md p-4 flex items-center space-x-4">
        <img
          src="https://via.placeholder.com/40"
          alt="User Avatar"
          className="h-10 w-10 rounded-full"
        />
        <h2 className="text-xl font-semibold text-gray-900">Alice</h2>
      </header>
      <main className="flex-1 overflow-y-auto bg-gray-100 p-4">
        {/* Chat messages */}
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'Alice' ? 'justify-start' : 'justify-end'}`}
            >
              <div className="flex items-start space-x-2">
                {message.sender === 'Alice' && (
                  <img
                    src="https://via.placeholder.com/40"
                    alt="Alice Avatar"
                    className="h-8 w-8 rounded-full"
                  />
                )}
                <div
                  className={`${
                    message.sender === 'Alice' ? 'bg-white text-gray-900' : 'bg-gray-800 text-white'
                  } p-4 rounded-lg shadow-md max-w-xs`}
                >
                  <p>{message.text}</p>
                </div>
                {message.sender !== 'Alice' && (
                  <img
                    src="https://via.placeholder.com/40"
                    alt="User Avatar"
                    className="h-8 w-8 rounded-full"
                  />
                )}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="flex items-center space-x-2">
                <img
                  src="https://via.placeholder.com/40"
                  alt="Alice Avatar"
                  className="h-8 w-8 rounded-full"
                />
                <div className="bg-white p-4 rounded-lg shadow-md max-w-xs">
                  <p className="text-gray-900">Alice is typing...</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <footer className="bg-white shadow-md p-4">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Type your message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className="flex-1 p-2 border border-gray-300 rounded-lg"
          />
          <button
            className="bg-gray-800 text-white p-3 rounded-full flex items-center justify-center"
            onClick={handleSend}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              className="h-6 w-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4l8 8-8 8M4 12h16"
              />
            </svg>
          </button>
        </div>
      </footer>
    </div>
  );
};

export default ChatPage;
