import { useEffect, useState } from "react";
import { activityApi } from "../api/activity";
import { formatActivity } from "../utils/activityFormat";

export default function ActivityFeed() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    activityApi
      .list()
      .then((res) => setItems(res.data.items))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="text-sm text-slate-500">
        Loading activity…
      </div>
    );
  }

  if (!items.length) {
    return (
      <div className="text-sm text-slate-500">
        No recent activity.
      </div>
    );
  }

  return (
    <ul className="space-y-2">
      {items.map((e) => (
        <li
          key={e.id}
          className="text-sm text-slate-700 flex gap-2"
        >
          <span>•</span>
          <span>{formatActivity(e)}</span>
          <span className="text-slate-400 text-xs">
            {new Date(e.created_at).toLocaleString()}
          </span>
        </li>
      ))}
    </ul>
  );
}

