import React from 'react';

const EmptyChat = () => {
  return (
    <div
      className='
        px-4
        py-10
        sm:px-6
        lg:px-8
        h-full
        flex 
        justify-center
        items-center
        bg-gradient-to-r
        from-blue-100
        via-blue-200
        to-blue-100
        animate-gradient
      '
    >
      <div className='text-center items-center flex flex-col'>
        <div
          className='
            flex 
            items-center
            justify-center
            h-16
            w-16
            sm:h-20
            sm:w-20
            rounded-full
            bg-blue-200
            mb-4
          '
        >
          <svg
            className='w-10 h-10 sm:w-12 sm:h-12 text-blue-600'
            fill='currentColor'
            viewBox='0 0 20 20'
            xmlns='http://www.w3.org/2000/svg'
          >
            <path
              fillRule='evenodd'
              d='M2 5a2 2 0 012-2h12a2 2 0 012 2v7a2 2 0 01-2 2H8l-4 4v-4H4a2 2 0 01-2-2V5zm12 4a1 1 0 100-2 1 1 0 000 2z'
              clipRule='evenodd'
            />
          </svg>
        </div>
        <h3
          className='
            mt-2 
            text-lg
            sm:text-xl
            font-semibold
            text-gray-900
          '
        >
          Select a chat or start a new conversation
        </h3>
        <p className='mt-1 text-gray-600 text-sm sm:text-base'>
          Choose from your existing conversations, or start a new one to connect with your contacts.
        </p>
        <button
          className='
            mt-4
            px-3
            py-2
            sm:px-4
            sm:py-2
            bg-blue-600
            text-white
            rounded-lg
            shadow
            hover:bg-blue-700
            focus:outline-none
            focus:ring-2
            focus:ring-blue-600
            focus:ring-opacity-50
          '
        >
          New Conversation
        </button>
      </div>
    </div>
  );
};

export default EmptyChat;
