import React from "react";

export default function DecorStudio({ decor = [] }) {
  if (!decor.length) {
    return <div>No decor applied</div>;
  }

  const grouped = decor.reduce((acc, item) => {
    acc[item.domain] = acc[item.domain] || [];
    acc[item.domain].push(item);
    return acc;
  }, {});

  return (
    <section aria-label="Decor Studio">
      <h2>Decor Studio</h2>

      {Object.entries(grouped).map(([domain, items]) => {
        const title = domain
          .split(".")
          .map((s) => s[0].toUpperCase() + s.slice(1))
          .join(" ");

        return (
          <section key={domain}>
            <h3>{title}</h3>

            <ul>
              {items.map((d) => (
                <li key={d.id}>
                  <div>{d.name}</div>
                  {d.source && (
                    <div data-testid="decor-source">
                      Source: {d.source}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </section>
  );
}

