export function useKernel() {
  return {
    mode: "editing",
    station: "geometry",
    canUseTool: (tool: string) => true,
    execute: async (command: any) => {
      throw new Error("Not implemented");
    },
    reportError: (msg: string) => {
      console.error(msg);
    },
  };
}

