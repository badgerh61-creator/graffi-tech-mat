// frontend/src/errors/PanelErrorBoundary.jsx

import React from "react";
import EditorErrorBoundary from "./EditorErrorBoundary";

export default function PanelErrorBoundary({
  panelId,
  panelTitle,
  children,
}) {
  return (
    <EditorErrorBoundary scope={`panel:${panelId}`}>
      <PanelFallbackWrapper panelTitle={panelTitle}>
        {children}
      </PanelFallbackWrapper>
    </EditorErrorBoundary>
  );
}

/**
 * Wrapper that provides panel-specific fallback UI
 * while delegating error capture to EditorErrorBoundary.
 */
class PanelFallbackWrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="panel-error-boundary p-3 text-sm text-ui-muted border border-ui-border rounded">
          <strong className="block mb-1">
            {this.props.panelTitle} failed to load
          </strong>
          <p>
            This panel encountered an error and has been disabled.
            Other panels and your workspace are unaffected.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

