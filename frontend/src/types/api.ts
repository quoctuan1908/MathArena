export type ApiResponse<T> = {
    status: number,
    message?: string,
    data: T
}

export interface RefreshResponse {
  token: string;
}