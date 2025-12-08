let ws: WebSocket | null = null;

export const getSocket = () => ws;
export const setSocket = (socket: WebSocket | null) => {
  ws = socket;
};
