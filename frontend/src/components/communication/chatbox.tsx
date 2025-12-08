import { useEffect, useRef } from "react";
import type { Message } from "../../types/message";
import MessageItem from "./messageItem";

type ChatBoxProps = {
  messages: Message[];
};

const ChatBox: React.FC<ChatBoxProps> = ({ messages }) => {
  const endRef = useRef<HTMLDivElement | null>(null);

  // Tự động scroll xuống cuối khi có tin nhắn mới
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      className="
        flex flex-col
        min-h-[85vh]
        overflow-y-auto scroll-smooth
        bg-gradient-to-b from-gray-50 to-gray-100
        p-4 space-y-2
      "
    >
      {messages.length > 0 ? (
        messages.map((msg) => (
          <MessageItem key={msg.message_id || Math.random()} message={msg} />
        ))
      ) : (
        <div className="flex items-center justify-center h-full text-gray-400 italic">
          No messages yet — start the conversation 💬
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
};

export default ChatBox;
