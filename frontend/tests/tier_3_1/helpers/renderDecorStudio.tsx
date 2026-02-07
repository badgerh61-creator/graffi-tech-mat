import React from "react";
import { render } from "@testing-library/react";
import DecorStudio from "@/editor/studio/DecorStudio";

let lastRender: ReturnType<typeof render> | null = null;

export function renderDecorStudio(props: { decor?: any[] }) {
  lastRender = render(<DecorStudio decor={props.decor ?? []} />);
  return lastRender;
}

export function rerenderDecorStudio(props: { decor?: any[] }) {
  if (!lastRender) {
    throw new Error("DecorStudio has not been rendered yet");
  }

  lastRender.rerender(<DecorStudio decor={props.decor ?? []} />);
}

