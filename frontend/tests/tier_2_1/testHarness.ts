import { vi } from "vitest"

/**
 * -----------------------------
 * Kernel mock
 * -----------------------------
 */
export const kernel = {
  execute: vi.fn(),
}

export function mockKernelExecute() {
  kernel.execute.mockResolvedValue({ ok: true })
}

export function mockKernelReject(message: string) {
  kernel.execute.mockRejectedValue(new Error(message))
}

/**
 * -----------------------------
 * Editor state (minimal)
 * -----------------------------
 */
let snapshotId = "snap_1"
let snapshotStatus: "draft" | "completed" = "draft"
let mode: "editing" | "viewing" = "editing"

/**
 * -----------------------------
 * Render stub
 * -----------------------------
 */
export function renderEditor(opts?: {
  snapshot?: { status?: "draft" | "completed" }
  mode?: "editing" | "viewing"
}) {
  snapshotStatus = opts?.snapshot?.status ?? "draft"
  mode = opts?.mode ?? "editing"

  document.body.innerHTML = `
    <button
      data-testid="transform-btn"
      ${snapshotStatus !== "draft" || mode !== "editing" ? "disabled" : ""}
    >
      Transform
    </button>
    <div id="errors"></div>
  `
}

/**
 * -----------------------------
 * UI helpers
 * -----------------------------
 */
export function getTransformButton(): HTMLButtonElement {
  const el = document.querySelector(
    '[data-testid="transform-btn"]'
  ) as HTMLButtonElement | null

  if (!el) {
    throw new Error("Transform button not rendered")
  }

  return el
}

export function clickTransformButton() {
  getTransformButton().click()
}

/**
 * -----------------------------
 * Transform submission (Tier 2.1 contract)
 * -----------------------------
 */
export async function submitTransform(params: any) {
  try {
    await kernel.execute({
      tool: "translate",
      params,
    })
  } catch (err: any) {
    const el = document.getElementById("errors")
    if (el) el.textContent = err.message
  }
}

/**
 * -----------------------------
 * Error helpers
 * -----------------------------
 */
export function getErrorText(): string {
  return document.getElementById("errors")?.textContent ?? ""
}

/**
 * -----------------------------
 * Snapshot helpers
 * -----------------------------
 */
export function getSnapshotId() {
  return snapshotId
}

