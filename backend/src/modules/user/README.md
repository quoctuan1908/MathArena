# User Management API

All endpoints are prefixed with `/users` and require a valid database session.

---

## 1. Create User
- **Method:** `POST`
- **Endpoint:** `/`
- **Description:** Creates a new user.
- **Body:** `UserCreate`
  - `username` (string, required)  
  - `password_hashed` (string, required)  
  - `user_info` (object, optional)  
  - `user_statistic` (object, optional)  
  - `user_role_id` (UUID, optional)
- **Response:** `200 OK`, `UserResponse`
- **Errors:** `400`, `500`

---

## 2. List Users
- **Method:** `GET`
- **Endpoint:** `/`
- **Description:** Lists all users.
- **Response:** `200 OK`, `List<UserResponse>`
- **Errors:** `500`

---

## 3. List User Roles
- **Method:** `GET`
- **Endpoint:** `/roles`
- **Description:** Lists all roles.
- **Response:** `200 OK`, `List<UserRoleResponse>`
- **Errors:** `500`

---

## 4. Update User Role
- **Method:** `PUT`
- **Endpoint:** `/roles/{user_role_id}`
- **Description:** Updates a role.
- **Params:**  
  - `user_role_id` (UUID, required)
- **Body:** `UserRoleUpdate`
  - `user_role_name` (string, optional)  
  - `user_role_description` (string, optional)
- **Response:** `200 OK`, `UserRoleResponse`
- **Errors:** `404`, `400`, `500`

---

## 5. Delete User Role
- **Method:** `DELETE`
- **Endpoint:** `/roles/{user_role_id}`
- **Description:** Deletes a role.
- **Params:**  
  - `user_role_id` (UUID, required)
- **Response:** `204 No Content`  
  > Note: Current return is `{"message": "User deleted"}`, consider returning `None`.
- **Errors:** `404`, `500`

---

## 6. Get User Statistics
- **Method:** `GET`
- **Endpoint:** `/stat/{user_id}`
- **Description:** Gets user statistics.
- **Params:**  
  - `user_id` (UUID, required)
- **Response:** `200 OK`, `UserStatisticResponse`
- **Errors:** `404`, `500`

---

## 7. Get User Info
- **Method:** `GET`
- **Endpoint:** `/info/{user_id}`
- **Description:** Gets user info.
- **Params:**  
  - `user_id` (UUID, required)
- **Response:** `200 OK`, `UserInfoResponse`  
  > Note: Current response uses `UserStatisticResponse`, fix needed.
- **Errors:** `404`, `500`

---

## 8. Update User Password
- **Method:** `PUT`
- **Endpoint:** `/{user_id}/password`
- **Description:** Updates user password with current password verification.
- **Params:**  
  - `user_id` (UUID, required)
- **Body:** `UserPasswordUpdate`
  - `current_password_hashed` (string, required)  
  - `password_hashed` (string, required)
- **Response:** `200 OK`, `UserResponse`
- **Errors:** `400`, `404`, `500`

---

## 9. Get User
- **Method:** `GET`
- **Endpoint:** `/{user_id}`
- **Description:** Gets user details.
- **Params:**  
  - `user_id` (UUID, required)
- **Response:** `200 OK`, `UserResponse`
- **Errors:** `404`, `500`

---

## 10. Update User
- **Method:** `PUT`
- **Endpoint:** `/{user_id}`
- **Description:** Updates user details.
- **Params:**  
  - `user_id` (UUID, required)
- **Body:** `UserUpdate`
  - `username` (string, optional)  
  - `is_enabled` (boolean, optional)  
  - `role_id` (UUID, optional)  
  - `user_info` (object, optional)  
  - `user_statistic` (object, optional)
- **Response:** `200 OK`, `UserResponse`
- **Errors:** `404`, `400`, `500`

---

## 11. Delete User
- **Method:** `DELETE`
- **Endpoint:** `/{user_id}`
- **Description:** Deletes a user.
- **Params:**  
  - `user_id` (UUID, required)
- **Response:** `204 No Content`  
  > Note: Current return is `{"message": "User deleted"}`, consider returning `None`.
- **Errors:** `404`, `500`

---
