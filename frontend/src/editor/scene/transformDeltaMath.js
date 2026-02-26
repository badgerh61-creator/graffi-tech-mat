export function dominantAxisFromEulerDelta({ dx, dy, dz }) {
  const ax = Math.abs(dx), ay = Math.abs(dy), az = Math.abs(dz);
  let axis = "y", degrees = dy;
  if (ax >= ay && ax >= az) { axis = "x"; degrees = dx; }
  else if (az >= ax && az >= ay) { axis = "z"; degrees = dz; }
  return { axis, degrees };
}
