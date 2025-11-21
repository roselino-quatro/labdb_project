'use client';

interface Message {
  category: 'success' | 'error' | 'warning' | 'info';
  text: string;
}

interface MessagesProps {
  messages?: Message[];
}

export default function Messages({ messages }: MessagesProps) {
  if (!messages || messages.length === 0) {
    return null;
  }

  return (
    <div className="mb-4 space-y-2">
      {messages.map((message, index) => {
        const bgColorClass =
          message.category === 'success'
            ? 'border-green-500 bg-green-50 text-green-800'
            : message.category === 'error'
            ? 'border-red-500 bg-red-50 text-red-800'
            : message.category === 'warning'
            ? 'border-yellow-500 bg-yellow-50 text-yellow-800'
            : 'border-[#1094ab] bg-[#64c4d2] text-[#1094ab]';

        return (
          <div
            key={index}
            className={`rounded border-l-4 p-4 ${bgColorClass}`}
          >
            {message.text}
          </div>
        );
      })}
    </div>
  );
}
