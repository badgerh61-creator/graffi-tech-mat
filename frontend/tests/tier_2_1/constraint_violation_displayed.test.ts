import {
  renderEditor,
  mockKernelReject,
  clickTransformButton,
  submitTransform,
  getErrorText,
} from "./testHarness"

test("constraint violation is shown", async () => {
  renderEditor()
  mockKernelReject("violates symmetry constraint")

  clickTransformButton()
  await submitTransform({ x: 5 })

  expect(getErrorText()).toMatch(/symmetry/i)
})

