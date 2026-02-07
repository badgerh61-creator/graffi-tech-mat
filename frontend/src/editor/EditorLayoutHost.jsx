import DecorStudio from "./studio/DecorStudio";
import { useDecor } from "./kernel/useDecor";

export function EditorLayoutHost() {
  const { decor } = useDecor();

  return (
    <>
      <DecorStudio decor={decor} />
    </>
  );
}

