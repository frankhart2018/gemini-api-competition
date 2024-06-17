import React from 'react'
import Sidebar from '../components/Sidebar'
import ChatPage from '../components/ChatPage'

const text = () => {
  return (
    <div className="h-screen flex">
      <Sidebar />
      <div className="flex-1">
        <ChatPage />
      </div>
    </div>
  )
}

export default text