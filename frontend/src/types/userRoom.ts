import type { RoomChat } from "./roomchat"

export type UserRoomRole = {
    user_room_role_id: string,
    user_room_role_name: string,
    user_room_role_description: string
}

export type UserRoom = {
    room_chat_id: string,
    user_id: string,
    user_room_role_id: string,
    room_chats: RoomChat 
}

export type UserRoomCreate = {
    room_chat_id: string,
    user_id: string,
    user_room_role_id: string
}