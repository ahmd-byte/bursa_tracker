import { Toaster } from "react-hot-toast";
import { Dashboard } from "./pages/Dashboard";

function App() {
  return (
    <>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 3000,
          style: {
            background: "rgba(255, 255, 255, 0.9)",
            backdropFilter: "blur(12px)",
            color: "#1e293b",
            padding: "16px 24px",
            borderRadius: "16px",
            border: "1px solid rgba(255, 255, 255, 0.3)",
            boxShadow: "0 10px 40px rgba(0, 0, 0, 0.1)",
            fontWeight: "500",
          },
          success: {
            iconTheme: {
              primary: "#10b981",
              secondary: "#fff",
            },
          },
          error: {
            iconTheme: {
              primary: "#ef4444",
              secondary: "#fff",
            },
          },
          loading: {
            iconTheme: {
              primary: "#6366f1",
              secondary: "#fff",
            },
          },
        }}
      />
      <Dashboard />
    </>
  );
}

export default App;
