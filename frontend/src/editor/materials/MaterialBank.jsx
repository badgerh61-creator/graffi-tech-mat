import { API_BASE } from "../../config/apiBase";

import { useEffect, useState } from "react";
import { MaterialCard } from "./MaterialCard";

export default function MaterialBank() {
  const [materials, setMaterials] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/materials`)
      .then((res) => res.json())
      .then((data) => {
        setMaterials(data.items);
      });
  }, []);

  return (
    <section>
      <h2>Material Bank</h2>
      {materials.map((m) => (
        <MaterialCard key={m.id} material={m} />
      ))}
    </section>
  );
}

