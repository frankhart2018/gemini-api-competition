"use client";

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

const Sidebar = () => {
  const dummyChats = [
    {
      id: 1,
      name: 'Alice',
      message: 'Hey, how are you?',
      avatar: 'https://via.placeholder.com/40',
      status: 'online',
    },
    {
      id: 2,
      name: 'Bob',
      message: 'Are we still meeting tomorrow?',
      avatar: 'https://via.placeholder.com/40',
      status: 'offline',
    },
    {
      id: 3,
      name: 'Charlie',
      message: 'Check out this link!',
      avatar: 'https://via.placeholder.com/40',
      status: 'online',
    },
  ];

  const getStatusColor = (status) => {
    return status === 'online' ? 'bg-green-500' : 'bg-gray-400';
  };

  return (
    <div className="relative h-full w-64 bg-gray-50 border-r border-gray-200 overflow-y-auto flex flex-col justify-between">
      <div>
        <div className="p-4">
          <h2 className="text-lg font-semibold text-gray-900">Chats</h2>
        </div>
        <ul>
          {dummyChats.map((chat) => (
            <li
              key={chat.id}
              className="flex items-center p-4 hover:bg-gray-300 cursor-pointer transition-colors duration-300"
            >
              <div className="relative">
                <img
                  src={chat.avatar}
                  alt={chat.name}
                  className="h-10 w-10 rounded-full mr-3"
                />
                <span
                  className={`absolute bottom-0 right-0 h-3 w-3 rounded-full border-2 border-white ${getStatusColor(
                    chat.status
                  )}`}
                />
              </div>
              <div className="flex flex-col">
                <span className="font-semibold text-gray-900">{chat.name}</span>
                <span className="text-gray-600 text-sm truncate">
                  {chat.message}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="p-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Avatar
              variant="square"  
            >
              <AvatarImage src="https://via.placeholder.com/40" alt="User Avatar" />
              <AvatarFallback>CU</AvatarFallback>
            </Avatar>
          </div>
          <div>
            <p className="font-semibold text-gray-900">Current User</p>
            <p className="text-sm text-gray-600">Online</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
