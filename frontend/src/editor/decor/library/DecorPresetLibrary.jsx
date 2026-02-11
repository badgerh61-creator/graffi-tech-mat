import { useEffect, useState } from "react";
import { DecorPresetCard } from "./DecorPresetCard";

export default function DecorPresetLibrary() {
  const [presets, setPresets] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/decor-presets")
      .then((res) => res.json())
      .then((data) => setPresets(data.items));
  }, []);

  return (
    <section>
      <h2>Decor Preset Library</h2>
      {presets.map((p) => (
        <DecorPresetCard key={p.id} preset={p} />
      ))}
    </section>
  );
}

