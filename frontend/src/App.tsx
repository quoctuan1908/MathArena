import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/homepage";
import { Header } from "./components/Header";
import { Footer } from "./components/Footer";
import LoginPage from "./pages/loginPage";
import SignUpPage from "./pages/signupPage";
import CommunicationPage from "./pages/communicationPage";
import { PublicRoute } from "./routers/PublicRoute";
import QuizPage from "./pages/quizPage";
import AdminRoute from "./routers/AdminRoute";
import AddQuestionsPage from "./pages/addQuestionPage";
import QuizListPage from "./pages/quizListPage";
import "./App.css";

function App() {
  return (
    <div className="flex min-h-screen w-full bg-gray-50 text-gray-900">
      {/* Sidebar cố định */}
      <aside className="md:flex fixed top-0 left-0 h-full bg-white shadow-sm flex-col z-20">
        <Header />
      </aside>

      {/* Nội dung chính */}
      <div className="flex flex-col flex-1 md:ml-53 h-screen min-h-0">
        {/* main phải có min-h-0 để overflow hoạt động */}
        <main className="flex-1 overflow-y-auto min-h-0 bg-gray-50 custom-scrollbar">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/communication/:id" element={<CommunicationPage />} />
            <Route path="/quiz_room" element={<QuizListPage />} />
            <Route path="/quiz_room/:id" element={<QuizPage />} />
            <Route
              path="/login"
              element={
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              }
            />
            <Route
              path="/questions"
              element={<AdminRoute element={<AddQuestionsPage />} />}
            />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/logout" element={<div></div>} />
          </Routes>
        </main>

        <footer className="hidden md:block bg-white p-4 text-center shadow-sm">
          <Footer />
        </footer>
      </div>
    </div>
  );
}

export default App;
