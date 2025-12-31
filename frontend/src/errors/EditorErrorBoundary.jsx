// frontend/src/errors/EditorErrorBoundary.jsx

import React from "react";

export default class EditorErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    // Week 8: console logging only (no telemetry yet)
    console.error("[EditorErrorBoundary]", {
      error,
      info,
      scope: this.props.scope || "unknown",
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="editor-error-boundary p-4 text-sm text-ui-muted">
          <strong className="block mb-1">
            Something went wrong.
          </strong>
          <p>
            This part of the editor failed to render.
            Other areas may still be working.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

