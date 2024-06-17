import React from 'react';
import Sidebar from './components/Sidebar'; 
import EmptyChat from './components/EmptyChat'; 

const Chat = () => {
  return (
    <div className="h-screen flex">
      <Sidebar />
      <div className="flex-1">
        <EmptyChat />
      </div>
    </div>
  );
};

export default Chat;
