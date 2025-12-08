import type { UserInfo } from "./user"

export interface QuestionType {
  id: number
  name: string
  description?: string | null
  created_at: string
  updated_at?: string | null
}

// ========== Subject ==========
export interface Subject {
  id: number
  name: string
  description?: string | null
  created_at: string
  updated_at?: string | null
}

// ========== Question ==========
export interface Question {
  id: string // UUID
  question_text: string
  answer?: string | null
  score: number

  question_type_id: number
  subject_id: number
  creator_id: string

  created_at: string
  updated_at?: string | null

  question_type?: QuestionType
  subject?: Subject
  creator?: UserSummary // để tránh import chéo nặng, dùng bản tóm tắt
}

export interface UserSummary {
  id: string
  username: string
  user_info?: UserInfo
}

export interface QuestionCreate {
  question_text: string
  answer?: string | null
  score: number

  question_type_id: number
  subject_id: number
  creator_id: string
}

export interface QuestionGenerate {
  text: string
}

export interface QuestionUpdate {
    payload: QuestionCreate,
    id: string
}

export interface GetQuestionsByCreatorParams {
  creatorId: string
  page: number
  limit: number
}

// Response structure for paginated questions
export interface PaginatedQuestionsResponse {
  items: Question[]
  total: number
}

export interface FastAnswerQuestion {
  room_id: string
  user_id: string,
  answer: string
}