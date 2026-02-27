import React from "react";

export default class ViewerErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error) {
    console.error("ViewerErrorBoundary caught:", error);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="border rounded p-3 text-sm text-red-700 space-y-2">
          <div className="font-semibold">Viewport crashed</div>
          <div className="opacity-80">
            {String(this.state.error?.message || this.state.error)}
          </div>
          <div className="text-xs opacity-70">
            Refresh the page to restore the viewport.
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
