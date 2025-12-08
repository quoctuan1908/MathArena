export interface SystemStats {
  total_users: number;
  total_rooms: number;
  total_messages: number;
  total_questions: number;
  average_users_per_room: number;
  total_score: number;
  average_user_score: number;
}

export interface UserStats {
  user_id: string;
  username: string;
  total_score: number;
  problem_solved: number;
  level: string | null;
}

export interface RoomStats {
  room_chat_id: string;
  room_name: string;
  room_type: string | null;
  total_users: number;
  total_messages: number;
  created_at: string;
  updated_at: string;
}