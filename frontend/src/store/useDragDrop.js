// src/store/useDragDrop.js
import { useEffect, useState } from "react";

export default function useDragDrop() {
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    let dragCounter = 0;

    const onDragEnter = (e) => {
      e.preventDefault();
      dragCounter++;
      setIsDragging(true);
    };

    const onDragLeave = (e) => {
      e.preventDefault();
      dragCounter--;
      if (dragCounter <= 0) setIsDragging(false);
    };

    const onDragOver = (e) => {
      e.preventDefault();
    };

    const onDrop = (e) => {
      e.preventDefault();
      dragCounter = 0;
      setIsDragging(false);
    };

    window.addEventListener("dragenter", onDragEnter);
    window.addEventListener("dragleave", onDragLeave);
    window.addEventListener("dragover", onDragOver);
    window.addEventListener("drop", onDrop);

    return () => {
      window.removeEventListener("dragenter", onDragEnter);
      window.removeEventListener("dragleave", onDragLeave);
      window.removeEventListener("dragover", onDragOver);
      window.removeEventListener("drop", onDrop);
    };
  }, []);

  return { isDragging };
}
