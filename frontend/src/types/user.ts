export interface UserInfo {
    name: string,
    birthday: string,
    address: string,
    phone: string,
    email: string,
    created_at: string
}

export interface LevelType {
    level_id: string, 
    level_type_name: string,
    level_type_description: string
}

export interface UserStatistic {
    level_id: string,
    problem_solved: number,
    score: number

}

export interface UserRole {
    user_role_id: string,
    user_role_name: string,
    user_role_description: string
}

export interface UserResponse {
    id: string, 
    username: string,
    is_enabled: boolean
    created_at: string,
    updated_at: string
    user_statistic: UserStatistic,
    user_info: UserInfo,
    user_role: UserRole

}

export interface UserCreate {
    username: string,
    password_hashed: string,
    user_info: UserInfo
}

