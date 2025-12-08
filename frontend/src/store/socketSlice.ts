import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { Question } from "../types/questions";
import type { UserResponse } from "../types/user";

interface QueuedMessage {
  event: string;
  payload: any;
}

interface UserInRoom extends UserResponse {
  room_score?: number; // điểm tạm trong phòng
}

interface SocketState {
  isConnected: boolean;
  room_id?: string;
  inRoom: boolean;
  queuedMessages: QueuedMessage[];
  roomUserCounts: Record<string, number>;

  // --- GAME STATE ---
  gameStatus: "idle" | "countdown" | "started" | "finished";
  countdownTime: number;
  currentQuestion: Question | null;
  players: UserInRoom[];
  allRooms: { room_id: string; count: number }[];
  questionIndex: number; 
  totalQuestions: number;     
  questions: Question[]

  lastEvent?: string;
  lastPayload?: any;
}

const initialState: SocketState = {
  isConnected: false,
  room_id: undefined,
  inRoom: false,
  queuedMessages: [],

  gameStatus: "idle",
  countdownTime: 0,
  currentQuestion: null,
  players: [],
  questionIndex: 0,
  totalQuestions: 0,
  questions: [],

  roomUserCounts: {},
  allRooms: [],
  lastEvent: undefined,
  lastPayload: undefined,
};

const socketSlice = createSlice({
  name: "socket",
  initialState,
  reducers: {
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
    setRoomId: (state, action: PayloadAction<string>) => {
      state.room_id = action.payload;
    },
    setLastMessage: (
      state,
      action: PayloadAction<{ event: string; payload: any }>
    ) => {
      state.lastEvent = action.payload.event;
      state.lastPayload = action.payload.payload;
    },
    clearRoomData: (state) => {
      state.inRoom = false;
      state.room_id = undefined;
      state.players = [];
      state.currentQuestion = null;
      state.countdownTime = 0;
    },
    queueMessage: (state, action: PayloadAction<QueuedMessage>) => {
      state.queuedMessages.push(action.payload);
    },
    clearQueuedMessages: (state) => {
      state.queuedMessages = [];
    },
    setPlayers: (state, action: PayloadAction<UserResponse[]>) => {
      state.players = action.payload;
    },

    // --- CẬP NHẬT GAME ---
    setGameStatus: (
      state,
      action: PayloadAction<"idle" | "countdown" | "started" | "finished">
    ) => {
      state.gameStatus = action.payload;
    },
    setGameCountdown: (state, action: PayloadAction<number>) => {
      state.gameStatus = "countdown";
      state.countdownTime = action.payload;
    },
    setGameStarted: (state) => {
      state.gameStatus = "started";
      state.countdownTime = 0;
    },
    setGameFinished: (
      state,
      action: PayloadAction<{
        scores: Record<string, number>;
        all_questions: Question[]
      }> // { [user_id]: total_score }
    ) => {
      state.gameStatus = "finished";

      const { scores, all_questions } = action.payload;
      state.questions = all_questions;
      // Gộp điểm vào từng player trong phòng
      state.players = state.players.map((p) => {
        const finalScore = scores[p.id];
        if (finalScore !== undefined) {
          return {
            ...p,
            room_score: finalScore,
          };
        }
        return p;
      });
    },
    setCurrentQuestion: (
      state,
      action: PayloadAction<{ question: Question; index: number; total: number }>
    ) => {
      state.currentQuestion = action.payload.question;
      state.questionIndex = action.payload.index;
      state.totalQuestions = action.payload.total;
    },
    updateScore: (
      state,
      action: PayloadAction<{ userId: string; score: number }>
    ) => {
      const { userId, score } = action.payload;
      const player = state.players.find((p) => p.id === userId);
      if (player) {
        player.room_score = (player.room_score ?? 0) + score;
      }
    },
    resetGameState: (state) => {
      state.gameStatus = "idle";
      state.currentQuestion = null;
      state.countdownTime = 0;
    },
    setRoomUserCount: (state, action: PayloadAction<{ room_id: string; count: number }>) => {
      const { room_id, count } = action.payload;
      state.roomUserCounts = {
        ...state.roomUserCounts,
        [room_id]: count,
      };
    },
    leaveRoom: (state, action: PayloadAction<string>) => {
      const roomId = action.payload;
      if (state.room_id === roomId) {
        state.inRoom = false;
        state.room_id = undefined;
        state.players = [];
      }
      delete state.roomUserCounts[roomId]; // xóa count của phòng này
    },
    setAllRooms(state, action: PayloadAction<{ room_id: string; count: number }[]>) {
      state.allRooms = action.payload;
    },
  },
});

export const {
  setConnected,
  setRoomId,
  setLastMessage,
  queueMessage,
  clearRoomData,
  clearQueuedMessages,
  setPlayers,
  setGameCountdown,
  setGameStarted,
  setGameFinished,
  setGameStatus,
  setCurrentQuestion,
  updateScore,
  resetGameState,
  setRoomUserCount,
  leaveRoom,
  setAllRooms,
} = socketSlice.actions;

export default socketSlice.reducer;
