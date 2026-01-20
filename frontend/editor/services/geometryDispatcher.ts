export class GeometryDispatcher {
  private commandLog: any[] = [];

  setParam(param: string, value: number) {
    this.dispatch({ command: "SET_PARAM", param, value });
  }

  segmentPanel(surface_id: string, bounds: string) {
    this.dispatch({ command: "SEGMENT_PANEL", surface_id, bounds });
  }

  dispatch(cmd: any) {
    this.commandLog.push(cmd);
    // send to engine bridge
  }

  lastCommand() {
    return this.commandLog[this.commandLog.length - 1];
  }
}

