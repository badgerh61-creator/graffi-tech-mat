// frontend/src/app/Sidebar.jsx

import React from "react";

export default function Sidebar() {
  return (
    <aside className="editor-sidebar">
      <ul className="sidebar-nav">
        <li className="sidebar-item active">Design</li>
        <li className="sidebar-item">Decor</li>
        <li className="sidebar-item">Tuning</li>
        <li className="sidebar-item">Testing</li>
      </ul>
    </aside>
  );
}

