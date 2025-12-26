import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api/client";

export default function AcceptInvite() {
  const { token } = useParams();
  const navigate = useNavigate();

  const [state, setState] = useState("loading"); // loading | success | error
  const [error, setError] = useState(null);

  useEffect(() => {
    async function acceptInvite() {
      try {
        await api.post(`/models/invites/${token}/accept`);
        setState("success");

        setTimeout(() => {
          navigate("/studio", { replace: true });
        }, 1500);
      } catch (err) {
        setState("error");
        setError(
          err?.response?.data?.detail ??
            "Invite is invalid or expired"
        );
      }
    }

    acceptInvite();
  }, [token, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white rounded-lg shadow p-6 w-full max-w-md text-center">
        {state === "loading" && (
          <>
            <div className="animate-spin mx-auto mb-4 w-6 h-6 border-2 border-slate-400 border-t-transparent rounded-full" />
            <p className="text-sm text-slate-600">
              Accepting invitation…
            </p>
          </>
        )}

        {state === "success" && (
          <>
            <h2 className="text-lg font-semibold mb-2">
              Invitation accepted 🎉
            </h2>
            <p className="text-sm text-slate-600">
              Redirecting to studio…
            </p>
          </>
        )}

        {state === "error" && (
          <>
            <h2 className="text-lg font-semibold mb-2 text-rose-600">
              Invitation failed
            </h2>
            <p className="text-sm text-slate-600 mb-4">
              {error}
            </p>
            <button
              onClick={() => navigate("/login")}
              className="px-4 py-2 rounded bg-slate-800 text-white text-sm hover:bg-slate-900"
            >
              Go to login
            </button>
          </>
        )}
      </div>
    </div>
  );
}

