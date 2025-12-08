import React from "react";
import type { Message } from "../../types/message";
import { useSelector } from "react-redux";
import type { RootState } from "../../store/store";

const MessageItem: React.FC<{ message: Message }> = ({ message }) => {
  const currentUser = useSelector((state: RootState) => state.auth.user);
  const isOwn = message.user_id === currentUser?.id;

  return (
    <div
      className={`flex items-end gap-2 mb-3 ${
        isOwn ? "justify-end" : "justify-start"
      }`}
    >
      {/* Avatar người khác */}
      {!isOwn && (
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-gray-400 to-gray-200 flex-shrink-0 shadow-sm" />
      )}

      {/* Nội dung tin nhắn */}
      <div
        className={`px-4 py-2 rounded-2xl max-w-[70%] shadow-sm transition-all duration-200
          ${
            isOwn
              ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-br-none hover:from-blue-600 hover:to-blue-700"
              : "bg-gray-100 text-gray-800 rounded-bl-none hover:bg-gray-200"
          }`}
      >
        <p className="text-sm leading-relaxed break-words">{message.message_text}</p>

        {message.user_id && (
          <p
            className={`text-xs mt-1 ${
              isOwn ? "text-blue-100 text-right" : "text-gray-500"
            }`}
          >
            @{message?.user.user_role.user_role_name == "admin" ? message?.user.user_role.user_role_name : message?.user.user_info.name}
          </p>
        )}
      </div>

      {/* Avatar của mình */}
      {isOwn && (
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-400 to-blue-300 flex-shrink-0 shadow-sm" />
      )}
    </div>
  );
};

export default MessageItem;
