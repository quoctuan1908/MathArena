import type { UserResponse } from "./user"

export type MessageType = {
    message_type_id: string,
    message_type_name: string,
    message_type_description: String
}

export type Message = {
    message_id: string,
    room_chat_id: string,
    user_id: string,
    message_type_id: string,
    message_text: string,
    reply_to_id: string,
    created_at: string,
    updated_at: string,
    user: UserResponse
    
}

export type MessageCreate = {
    room_chat_id: string,
    user_id: string,
    message_type_id: string,
    message_text: string,
    reply_to_id: string
}

export type SocketEvent =  {
    event: string,
    
}