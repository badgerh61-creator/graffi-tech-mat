import React from "react";

export default class CanvasBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { crashed: false };
  }

  static getDerivedStateFromError() {
    return { crashed: true };
  }

  componentDidCatch(err) {
    console.error("🔥 Canvas crashed:", err);
  }

  render() {
    if (this.state.crashed) {
      return (
        <div style={{ padding: 40, color: "#991b1b" }}>
          <h2>3D Engine Failed to Load</h2>
          <p>
            WebGL could not initialize on this device.
            The rest of the app is still usable.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

