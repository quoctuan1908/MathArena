import type { UserResponse } from "./user";

export type LoginResponse = {
    token: string;
    user: UserResponse;    
}

export type UserLogin = {
    username: string,
    password: string
}