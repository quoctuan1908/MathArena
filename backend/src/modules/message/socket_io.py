from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
from sqlalchemy.orm import Session
from src.database.core import SessionLocal
from src.database.socket_context import get_db_context
from . import model
from .service import create_message
from src.modules.question.service import get_random_questions
from src.modules.user.service import update_user_stat
from src.modules.user import model as user_model

rooms: Dict[str, Dict[str, Any]] = {} 
# { room_id: {"clients": [], "questions": [], "scores": {}, "current_question": None} }

async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("✅ Client connected")

    db: Session = SessionLocal()
    room_id = None
    user_info = None

    try:
        while True:
            data = json.loads(await ws.receive_text())
            event = data.get("event")
            payload = data.get("payload")
            print("⚡ Event:", event)

            # ===========================================================
            # 1️⃣ JOIN ROOM
            # ===========================================================
            if event == "join_room":
                room_id = payload.get("room_id")
                user_info = payload.get("user")
                user_id = str(user_info.get("id")) if user_info else None

                if not room_id or not user_info:
                    await ws.send_text(json.dumps({
                        "event": "error",
                        "payload": {"message": "Missing room_id or user info"}
                    }))
                    continue

                # --- Khởi tạo room nếu chưa có ---
                rooms.setdefault(room_id, {
                    "clients": [],
                    "questions": [],
                    "scores": {},
                    "current_question": None,
                    "answered_users": set()
                })

                # --- Thêm user vào room ---
                rooms[room_id]["clients"].append({"ws": ws, "user": user_info})

                # --- Khởi tạo điểm ---
                if user_id not in rooms[room_id]["scores"]:
                    rooms[room_id]["scores"][user_id] = 0

                # --- Danh sách user trong phòng ---
                users_in_room = [c["user"] for c in rooms[room_id]["clients"]]

                # --- Payload phản hồi cho user vừa join ---
                joined_payload = {
                    "event": "joined",
                    "payload": {
                        "room_id": room_id,
                        "users": users_in_room,
                        "count": len(users_in_room)
                    }
                }

                # ✅ Nếu là quiz-room → gửi thêm danh sách các phòng hiện có
                if room_id == "quiz-room":
                    room_summary = [
                        {"room_id": rid, "count": len(info["clients"])}
                        for rid, info in rooms.items()
                        if rid != "quiz-room"
                    ]
                    joined_payload["payload"]["rooms"] = room_summary

                await ws.send_text(json.dumps(joined_payload, default=str))

                # --- Gửi thông báo cho các user khác trong cùng phòng ---
                for client in rooms[room_id]["clients"]:
                    if client["ws"] != ws:
                        await client["ws"].send_text(json.dumps({
                            "event": "user_joined",
                            "payload": {"room_id": room_id, "users": users_in_room, "count": len(users_in_room)}
                        }, default=str))

                # --- Cập nhật số người cho quiz-room ---
                if "quiz-room" in rooms:
                    count = len(rooms[room_id]["clients"])
                    for client in rooms["quiz-room"]["clients"]:
                        await client["ws"].send_text(json.dumps({
                            "event": "update_user_count",
                            "payload": {"room_id": room_id, "users": users_in_room, "count": count}
                        }, default=str))
            # ===========================================================
            # 2️⃣ CHAT MESSAGE
            # ===========================================================
            if event == "send_message":
                with get_db_context() as db:
                    message_data = model.MessageCreate(**payload)
                    created_message = create_message(db=db, message_data=message_data)
                    response_data = model.MessageResponse.model_validate(created_message).model_dump()

                for client in rooms.get(room_id, {}).get("clients", []):
                    await client["ws"].send_text(json.dumps({
                        "event": "receive_message",
                        "payload": response_data
                    }, default=str))
                continue

            # ===========================================================
            # 3️⃣ START GAME
            # ===========================================================
            if event == "start_game":
                room_id_to_start = payload.get("room_id")
                if not room_id_to_start or room_id_to_start not in rooms:
                    await ws.send_text(json.dumps({
                        "event": "error",
                        "payload": {"message": "Invalid room to start"}
                    }))
                    continue

                print(f"🚀 Starting game in room {room_id_to_start}")

                # Đếm ngược
                for i in range(5, 0, -1):
                    countdown_payload = {
                        "event": "game_countdown",
                        "payload": {"time": i}
                    }
                    for client in rooms[room_id_to_start]["clients"]:
                        await client["ws"].send_text(json.dumps(countdown_payload))
                    await asyncio.sleep(1)

                # Lấy danh sách câu hỏi
                with get_db_context() as db_session:
                    question_batch = get_random_questions(db_session)

                if not question_batch:
                    await ws.send_text(json.dumps({
                        "event": "error",
                        "payload": {"message": "No questions available"}
                    }))
                    continue

                rooms[room_id_to_start]["questions"] = question_batch
                rooms[room_id_to_start]["current_index"] = 1  # ✅ bắt đầu từ câu 1

                first_question = rooms[room_id_to_start]["questions"].pop(0)
                rooms[room_id_to_start]["current_question"] = first_question

                # Gửi câu hỏi đầu tiên
                question_as_dict = {
                    "id": first_question.id,
                    "question_text": first_question.question_text,
                    "answer": first_question.answer,
                    "score": first_question.score,
                    "question_type_id": first_question.question_type_id,
                    "subject_id": first_question.subject_id,
                    "creator_id": first_question.creator_id,
                }

                payload_send = {
                    "event": "quiz_update_question",
                    "payload": {
                        "question": question_as_dict,
                        "room_id": room_id_to_start,
                        "current_index": rooms[room_id_to_start]["current_index"],  # ✅ gửi thêm index
                        "total_questions": len(question_batch) + 1  # ✅ tổng câu hỏi (đã trừ 1 khi pop)
                    }
                }
                for client in rooms[room_id_to_start]["clients"]:
                    await client["ws"].send_text(json.dumps(payload_send, default=str))
                continue


            # ===========================================================
            # 4️⃣ SUBMIT ANSWER
            # ===========================================================
            if event == "submit_answer":
                user_id = str(payload.get("user_id"))
                answer = payload.get("answer")
                room_id_submit = payload.get("room_id")

                if not room_id_submit or room_id_submit not in rooms:
                    await ws.send_text(json.dumps({
                        "event": "error",
                        "payload": {"message": "Invalid room"}
                    }))
                    continue

                room = rooms[room_id_submit]
                current_q = room.get("current_question")
                if not current_q:
                    continue

                correct_answer = str(current_q.answer).strip().lower()
                player_answer = str(answer).strip().lower()
                correct = player_answer == correct_answer
                score_gain = current_q.score if correct else 0

                # --- Cập nhật điểm trong bộ nhớ ---
                room["scores"].setdefault(user_id, 0)
                room["scores"][user_id] += score_gain
                total_score = room["scores"][user_id]

                # ✅ Nếu trả lời đúng -> cập nhật DB
                if correct:
                    try:
                        with get_db_context() as db_sess:
                            stat_data = user_model.StatUpdate(
                                added_score=score_gain,
                                added_solved=1
                            )
                            update_user_stat(db=db_sess, user_id=user_id, stat_data=stat_data)
                    except Exception as e:
                        print(f"⚠️ Lỗi khi cập nhật user stat: {e}")

                # --- Ghi lại người đã trả lời ---
                room.setdefault("answered_users", set())
                room["answered_users"].add(user_id)

                # --- Gửi kết quả cho người chơi ---
                personal_result = {
                    "event": "answer_result",
                    "payload": {
                        "user_id": user_id,
                        "correct": correct,
                        "added_score": score_gain,
                        "total_score": total_score
                    }
                }
                await ws.send_text(json.dumps(personal_result, default=str))

                # --- Gửi thông báo cho người khác ---
                broadcast_message = {
                    "event": "player_answered",
                    "payload": {
                        "user_id": user_id,
                        "correct": correct
                    }
                }
                for client in room["clients"]:
                    if client["ws"] != ws:
                        await client["ws"].send_text(json.dumps(broadcast_message, default=str))

                # --- Kiểm tra: tất cả đã trả lời? ---
                total_players = len([c for c in room["clients"] if not c.get("is_admin")])
                answered_players = len(room["answered_users"])

                if answered_players >= total_players:
                    # ---------------------------------------------------------
                    # [MỚI] Lưu câu hỏi vừa chơi xong vào danh sách đã chơi
                    # ---------------------------------------------------------
                    if "played_questions" not in room:
                        room["played_questions"] = []
                    
                    # Lưu câu hỏi hiện tại vào lịch sử trước khi chuyển câu mới
                    if room.get("current_question"):
                        room["played_questions"].append(room["current_question"])
                    # ---------------------------------------------------------

                    room["answered_users"] = set()
                    await asyncio.sleep(1.5)

                    if room["questions"]:
                        next_q = room["questions"].pop(0)
                        room["current_question"] = next_q
                        room["current_index"] += 1 

                        payload_send = {
                            "event": "quiz_update_question",
                            "payload": {
                                "question": {
                                    "id": next_q.id,
                                    "question_text": next_q.question_text,
                                    "answer": next_q.answer,
                                    "score": next_q.score,
                                    "question_type_id": next_q.question_type_id,
                                    "subject_id": next_q.subject_id,
                                    "creator_id": next_q.creator_id
                                },
                                "room_id": room_id_submit,
                                "current_index": room["current_index"],
                                "total_questions": room["current_index"] + len(room["questions"])
                            }
                        }
                        for client in room["clients"]:
                            await client["ws"].send_text(json.dumps(payload_send, default=str))
                    else:
                        scores = room["scores"]
                        
                        # ---------------------------------------------------------
                        # [MỚI] Chuẩn bị danh sách toàn bộ câu hỏi kèm đáp án
                        # ---------------------------------------------------------
                        full_questions_data = []
                        for q in room.get("played_questions", []):
                            full_questions_data.append({
                                "id": q.id,
                                "question_text": q.question_text,
                                "answer": q.answer,  # Đảm bảo trả về đáp án
                                "score": q.score,
                                "question_type_id": q.question_type_id
                                # Thêm các trường khác nếu cần thiết
                            })

                        end_payload = {
                            "event": "game_finished",
                            "payload": {
                                "scores": scores,
                                "all_questions": full_questions_data  # Gửi kèm bộ câu hỏi
                            }
                        }
                        # ---------------------------------------------------------

                        for client in room["clients"]:
                            await client["ws"].send_text(json.dumps(end_payload, default=str))
                continue

            # ===========================================================
            # 5️⃣ NEXT QUESTION (thủ công)
            # ===========================================================
            if event == "next_question":
                room_id_next = payload.get("room_id")

                if not room_id_next or room_id_next not in rooms:
                    await ws.send_text(json.dumps({
                        "event": "error",
                        "payload": {"message": "Invalid room"}
                    }))
                    continue

                if not rooms[room_id_next]["questions"]:
                    scores = rooms[room_id_next]["scores"]
                    end_payload = {
                        "event": "game_finished",
                        "payload": {"scores": scores}
                    }
                    for client in rooms[room_id_next]["clients"]:
                        await client["ws"].send_text(json.dumps(end_payload, default=str))
                    continue

                # Lấy câu tiếp theo
                next_q = rooms[room_id_next]["questions"].pop(0)
                rooms[room_id_next]["current_question"] = next_q
                rooms[room_id_next]["current_index"] += 1  # ✅ tăng thứ tự câu hỏi

                question_as_dict = {
                    "id": next_q.id,
                    "question_text": next_q.question_text,
                    "answer": next_q.answer,
                    "score": next_q.score,
                    "question_type_id": next_q.question_type_id,
                    "subject_id": next_q.subject_id,
                    "creator_id": next_q.creator_id
                }

                payload_send = {
                    "event": "quiz_update_question",
                    "payload": {
                        "question": question_as_dict,
                        "room_id": room_id_next,
                        "current_index": rooms[room_id_next]["current_index"],
                        "total_questions": rooms[room_id_next]["current_index"] + len(rooms[room_id_next]["questions"])
                    }
                }

                for client in rooms[room_id_next]["clients"]:
                    await client["ws"].send_text(json.dumps(payload_send, default=str))
                continue

    # ===========================================================
    # 6️⃣ HANDLE DISCONNECT
    # ===========================================================
    except WebSocketDisconnect:
        print(f"❌ Client disconnected from room: {room_id}")
        if room_id and rooms.get(room_id):
            rooms[room_id]["clients"] = [c for c in rooms[room_id]["clients"] if c["ws"] != ws]
            users_in_room = [u["user"] for u in rooms[room_id]["clients"]]

            for client in rooms.get(room_id, {}).get("clients", []):
                await client["ws"].send_text(json.dumps({
                    "event": "user_left",
                    "payload": {"room_id": room_id, "users": users_in_room, "count": len(users_in_room)}
                }))
                
            if room_id != "quiz-room":
                # broadcast đến quiz-room để cập nhật số người trong phòng
                if "quiz-room" in rooms:
                    count = len(rooms[room_id]["clients"])
                    for client in rooms["quiz-room"]["clients"]:
                        await client["ws"].send_text(json.dumps({
                            "event": "update_user_count",
                            "payload": {"room_id": room_id, "users": users_in_room, "count": len(users_in_room)}
                        }, default=str))
                        
            if not rooms[room_id]["clients"]:
                print(f"💀 Deleting empty room {room_id}")
                del rooms[room_id]
