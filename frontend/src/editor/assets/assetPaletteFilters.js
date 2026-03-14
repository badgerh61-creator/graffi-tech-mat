export function sortAssetsStable(assets = []) {
  return [...assets].sort((a, b) =>
    String(a?.id || "").localeCompare(String(b?.id || ""))
  );
}

export function filterAssets({
  assets = [],
  query = "",
  category = "all",
  favorites = [],
  mode = "all",
  recent = [],
}) {
  let out = sortAssetsStable(assets);

  if (mode === "favorites") {
    const favSet = new Set((favorites || []).map(String));
    out = out.filter((a) => favSet.has(String(a.id)));
  }

  if (mode === "recent") {
    const recentSet = new Set((recent || []).map(String));
    out = out.filter((a) => recentSet.has(String(a.id)));

    out.sort((a, b) => {
      const ai = recent.indexOf(String(a.id));
      const bi = recent.indexOf(String(b.id));
      if (ai !== bi) return ai - bi;
      return String(a.id).localeCompare(String(b.id));
    });
  }

  if (category !== "all") {
    out = out.filter((a) => String(a.category || "uncategorized") === String(category));
  }

  const q = String(query || "").trim().toLowerCase();
  if (q) {
    out = out.filter((a) =>
      String(a.id || "").toLowerCase().includes(q) ||
      String(a.name || "").toLowerCase().includes(q) ||
      String(a.kind || "").toLowerCase().includes(q) ||
      String(a.category || "").toLowerCase().includes(q) ||
      (a.tags || []).join(" ").toLowerCase().includes(q)
    );
  }

  return out;
}

export function listCategories(assets = []) {
  const cats = [...new Set((assets || []).map((a) => String(a.category || "uncategorized")))];
  return ["all", ...cats.sort((a, b) => a.localeCompare(b))];
}
