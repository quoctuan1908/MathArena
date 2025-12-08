import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { API_URL } from '../config/api';
import { type UserCreate, type UserResponse } from '../types/user';
import type { LoginResponse, UserLogin } from '../types/auth';
import type { Message, MessageCreate, MessageType } from '../types/message';
import type { ApiResponse } from '../types/api';
import type { RootState } from './store';
import type { UserRoom, UserRoomCreate } from '../types/userRoom';
import type {
  GetQuestionsByCreatorParams,
  PaginatedQuestionsResponse,
  Question,
  QuestionCreate,
  QuestionGenerate,
  QuestionType,
  QuestionUpdate,
  Subject,
} from '../types/questions';
import type { RoomChat, RoomChatCreate, RoomType } from '../types/roomchat';
import type { RoomStats, SystemStats, UserStats } from '../types/statistic';

interface LeaveRoomRequest {
  user_id: string;
  room_chat_id: string;
}

interface UpdateScoreRequest {
  user_id: string;
  added_score: number;
}

export const apiSlice = createApi({
  reducerPath: '/',
  baseQuery: fetchBaseQuery({
    baseUrl: API_URL,
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;

      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
      headers.set('Content-Type', 'application/json');
      return headers;
    },
  }),

  endpoints: (builder) => ({
    // ========================= USERS =========================
    getUsers: builder.query<UserResponse[], void>({
      query: () => 'users/',
    }),

    createUser: builder.mutation<UserCreate, Partial<UserCreate>>({
      query: (newUser) => ({
        url: 'users',
        method: 'POST',
        body: newUser,
      }),
    }),

    loginUser: builder.mutation<LoginResponse, UserLogin>({
      query: (loginData) => ({
        url: 'auth/login',
        method: 'POST',
        body: loginData,
      }),
    }),

    updateUserScore: builder.mutation<ApiResponse<boolean>, UpdateScoreRequest>({
      query: (updateScoreRequest) => ({
        url: `/users/stat/${updateScoreRequest.user_id}`,
        method: 'PATCH',
        body: updateScoreRequest,
      }),
    }),

    // ========================= STATISTICS =========================
    getSystemStats: builder.query<SystemStats, void>({
      query: () => '/users/system',
    }),

    getUserStats: builder.query<UserStats, string>({
      query: (userId) => `/users/user/${userId}`,
    }),

    getRoomStats: builder.query<RoomStats, string>({
      query: (roomChatId) => `/users/room/${roomChatId}`,
    }),

    // ========================= ROOMS =========================
    getRoomChats: builder.query<RoomChat[], void>({
      query: () => 'rooms/chats',
    }),

    getRoomChatByName: builder.query<RoomChat, string>({
      query: (name) => `rooms/chats/name/${name}`,
    }),

    getRoomChatById: builder.query<RoomChat, string>({
      query: (id) => `rooms/chats/${id}`,
    }),

    getRoomChatCentral: builder.query<RoomChat | null, void>({
      query: () => 'rooms/chats/central',
    }),

    getRoomQuiz: builder.query<RoomChat[], void>({
      query: () => 'rooms/quiz',
    }),

    getRoomChatTypes: builder.query<RoomType[], void>({
      query: () => 'rooms/types',
    }),

    createRoomChat: builder.mutation<ApiResponse<RoomChat>, RoomChatCreate>({
      query: (newRoom) => ({
        url: '/rooms/chats',
        method: 'POST',
        body: newRoom,
      }),
    }),

    // ========================= USER_ROOMS =========================
    getUserRoomByUserId: builder.query<UserRoom[], string>({
      query: (id) => `user_rooms/user/${id}`,
    }),

    joinRoom: builder.mutation<UserRoom, UserRoomCreate>({
      query: (joinRoomRequest) => ({
        url: '/user_rooms',
        method: 'POST',
        body: joinRoomRequest,
      }),
    }),

    leaveRoom: builder.mutation<UserRoom, LeaveRoomRequest>({
      query: (leaveRoomRequest) => ({
        url: `/user_rooms/${leaveRoomRequest.room_chat_id}/${leaveRoomRequest.user_id}`,
        method: 'DELETE',
        body: leaveRoomRequest,
      }),
    }),

    // ========================= MESSAGES =========================
    getMessageTypes: builder.query<MessageType[], void>({
      query: () => 'messages/types',
    }),

    getMessageByRoomChatId: builder.query<Message[], string>({
      query: (id) => `messages/room/${id}`,
    }),

    createMessage: builder.mutation<ApiResponse<Message>, MessageCreate>({
      query: (messageData) => ({
        url: 'messages',
        method: 'POST',
        body: messageData,
      }),
    }),

    // ========================= QUESTIONS =========================
    getQuestionsByCreatorId: builder.query<PaginatedQuestionsResponse, GetQuestionsByCreatorParams>({
      query: ({ creatorId, page, limit }) =>
        `/questions/creator/${creatorId}?page=${page}&limit=${limit}`,
    }),

    getQuestionTypes: builder.query<QuestionType[], void>({
      query: () => 'questions/types',
    }),

    getSubjects: builder.query<Subject[], void>({
      query: () => 'questions/subjects',
    }),

    getRandomQuestion: builder.query<Question, void>({
      query: () => '/questions/random',
    }),

    generateQuestion: builder.mutation<string, QuestionGenerate>({
      query: (newQuestion) => ({
        url: 'questions/generate',
        method: 'POST',
        body: newQuestion,
      }),
    }),

    createQuestion: builder.mutation<ApiResponse<Question>, QuestionCreate>({
      query: (newQuestion) => ({
        url: 'questions',
        method: 'POST',
        body: newQuestion,
      }),
    }),

    updateQuestion: builder.mutation<ApiResponse<Question>, QuestionUpdate>({
      query: (question) => ({
        url: `questions/${question.id}`,
        method: 'PUT',
        body: question.payload,
      }),
    }),
  }),
});

export default apiSlice;
