import { useEffect, useState } from "react";
import { Button } from "../Button";
import { Input } from "../Input";
import type { MessageCreate } from "../../types/message";
import apiSlice from "../../store/apiSlice";
import type { RoomChat } from "../../types/roomchat";
import { useSelector } from "react-redux";
import type { RootState } from "../../store/store";
import { useNavigate } from "react-router-dom";

type MessageBoxType = {
  onSend: (msg: MessageCreate) => void;
  room_data: RoomChat | null | undefined;
};

const MessageBox: React.FC<MessageBoxType> = ({ onSend, room_data }) => {
  const user = useSelector((state: RootState) => state.auth.user);
  const { data: messageTypes = [] } = apiSlice.endpoints.getMessageTypes.useQuery();
  const navigate = useNavigate();
  const [msg, setMessage] = useState<MessageCreate>({} as MessageCreate);

  useEffect(() => {
    if (room_data && user) {
      setMessage((prev) => ({
        ...prev,
        room_chat_id: room_data.room_chat_id,
        user_id: user.id,
      }));
    }
  }, [room_data, user]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!user) navigate("/login");
    onSend(msg);
    setMessage({ ...msg, message_text: "" });
  };

  const handleChangeText = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage((prev) => ({ ...prev, message_text: e.target.value }));
  };

  const handleChangeType = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setMessage((prev) => ({ ...prev, message_type_id: e.target.value }));
  };

  return (
    <div className="w-full mt-2">
      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 bg-white shadow-sm rounded-lg p-2 w-full"
      >
        {/* Select message type */}
        <select
          value={msg.message_type_id}
          onChange={handleChangeType}
          className="border border-gray-300 rounded-md px-2 py-1 text-md focus:ring-1 focus:ring-blue-400 focus:border-blue-400 outline-none transition-all"
        >
          {messageTypes.map((type) => (
            <option key={type.message_type_id} value={type.message_type_id}>
              {type.message_type_name}
            </option>
          ))}
        </select>

        {/* Input message */}
        <Input
          type="text"
          value={msg.message_text || ""}
          name="input"
          onChange={handleChangeText}
          placeholder="Nhập tin nhắn..."
          className="flex-1 border border-gray-300 rounded-md px-2 py-1 text-md focus:ring-1 focus:ring-blue-400 focus:border-blue-400 outline-none transition-all"
        />

        {/* Send button */}
        <Button
          type="submit"
          className="bg-blue-600 text-white px-3 py-1 rounded-md text-md font-medium hover:bg-blue-700 focus:ring-1 focus:ring-blue-400 transition-all"
        >
          Gửi
        </Button>
      </form>
    </div>

  );
};

export default MessageBox;


