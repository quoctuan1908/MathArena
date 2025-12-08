export type RoomType = {
    room_type_id: string,
    room_type_name: string,
    room_type_descryption: string
}

export type RoomChat = {
    room_chat_id: string,
    room_name: string,
    room_capacity: number | null,
    room_type_id: number,
    room_password: string | null,
    room_type: RoomType
}

export type RoomChatCreate = {
    room_name: string,
    room_capacity: number | null,
    room_type_id: number,
    room_password: string | null,
    host_id: string
}
