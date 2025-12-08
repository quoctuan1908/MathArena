import React, { useEffect, useRef, useState } from "react";
import type { UserResponse } from "../../types/user";

interface UserScore {
  user_id: string;
  score: number;
}

interface PlayerBoxProps {
  players: UserResponse[];
  playersScore: UserScore[];
}

interface Feedback {
  status: "correct" | "wrong";
  timestamp: number;
}

const PlayerBox: React.FC<PlayerBoxProps> = ({ players, playersScore }) => {
  const [feedback, setFeedback] = useState<Record<string, Feedback | null>>({});
  const prevScores = useRef<Record<string, number>>({});

  // 🧠 Theo dõi thay đổi điểm
  useEffect(() => {
    const now = Date.now();
    let hasChange = false;

    playersScore.forEach(({ user_id, score: newScore }) => {
      const oldScore = prevScores.current[user_id];

      if (oldScore === undefined) {
        prevScores.current[user_id] = newScore;
        return;
      }

      if (newScore !== oldScore) {
        const isCorrect = newScore > oldScore;
        prevScores.current[user_id] = newScore;
        hasChange = true;

        setFeedback((prev) => ({
          ...prev,
          [user_id]: { status: isCorrect ? "correct" : "wrong", timestamp: now },
        }));
      }
    });

    if (!hasChange) return;
  }, [playersScore]);

  // ⏱️ Tự động xóa feedback sau 3 giây
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setFeedback((prev) => {
        const updated = { ...prev };
        let changed = false;

        for (const [id, fb] of Object.entries(prev)) {
          if (fb && now - fb.timestamp > 3000) {
            updated[id] = null;
            changed = true;
          }
        }
        return changed ? updated : prev;
      });
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className="
        fixed right-2 top-20 z-40
        w-32 sm:w-32 md:w-32 lg:w-72
        p-3 sm:p-4 bg-white shadow-lg rounded-2xl border border-gray-100
        overflow-y-auto max-h-[70vh] sm:max-h-[80vh]
        transition-all duration-300
      "
    >
      <h2 className="font-semibold text-base sm:text-lg mb-3 text-center text-gray-700">
        Danh sách người chơi
      </h2>

      {players.length === 0 ? (
        <p className="text-gray-500 text-center italic">Chưa có người chơi</p>
      ) : (
        <div className="space-y-2 sm:space-y-3">
          {players.map((p) => {
            const score =
              playersScore.find((s) => s.user_id === p.id)?.score ??
              p.user_statistic.score ??
              0;
            const fb = feedback[p.id];

            return (
              <div
                key={p.id}
                className={`
                  relative flex justify-between items-center 
                  p-1.5 sm:p-2 rounded-lg text-xs sm:text-sm md:text-base
                  transition-all duration-200
                  ${
                    p.user_role.user_role_name === "admin"
                      ? "bg-gradient-to-r from-yellow-100 to-yellow-50 font-semibold text-yellow-700"
                      : "hover:bg-gray-50 border border-gray-100"
                  }
                `}
              >
                <span className="truncate max-w-[60%] sm:max-w-[70%]">
                  {p.user_role.user_role_name === "admin"
                    ? "👑 " + p.user_role.user_role_name
                    : p.user_info.name}
                </span>

                {p.user_role.user_role_name !== "admin" && (
                  <span className="font-bold text-gray-700">{score}</span>
                )}

                {fb && (
                  <span
                    className={`
                      absolute right-2 top-1/2 -translate-y-1/2
                      text-sm sm:text-base font-semibold transition-all duration-300
                      ${fb.status === "correct" ? "text-green-600" : "text-red-600"}
                    `}
                  >
                    {fb.status === "correct" ? "✅" : "❌"}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );

};

export default PlayerBox;
