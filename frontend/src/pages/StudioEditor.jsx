// frontend/src/pages/StudioEditor.jsx
import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getCurrentUser } from "../utils/auth";

export default function StudioEditor() {
  const user = getCurrentUser();

  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell>
        <EditorLayoutHost />
      </EditorShell>
    </CapabilityProvider>
  );
}

