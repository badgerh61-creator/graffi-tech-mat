// src/layout/Layout.jsx
import React from 'react'
import Topbar from '../ui/Topbar'
import Sidebar from '../ui/Sidebar'
import '../styles/index.css'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
