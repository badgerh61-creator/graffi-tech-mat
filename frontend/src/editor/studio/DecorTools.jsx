export function DecorTools({ canEdit }) {
  if (!canEdit) return null;

  return (
    <section>
      <button>Apply Material</button>
      <button>Replace Preset</button>
    </section>
  );
}

