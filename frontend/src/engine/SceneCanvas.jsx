// src/engine/SceneCanvas.jsx
import React, {
  forwardRef,
  useRef,
  useImperativeHandle,
  Suspense,
} from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, Line } from "@react-three/drei";
import ModelLoader from "./ModelLoader";
import { useModelStore } from "../store/modelStore";

/* ========================== GRID FLOOR ========================== */
function WireGrid() {
  const size = 30;
  const divisions = 30;
  const lines = [];

  for (let i = -divisions; i <= divisions; i++) {
    const pos = (i * size) / divisions;
    const fade = 0.15 + (0.85 * (divisions - Math.abs(i))) / divisions;

    lines.push(
      <React.Fragment key={i}>
        <Line
          points={[
            [pos, 0, -size],
            [pos, 0, size],
          ]}
          color="#40587d"
          transparent
          opacity={fade}
        />
        <Line
          points={[
            [-size, 0, pos],
            [size, 0, pos],
          ]}
          color="#40587d"
          transparent
          opacity={fade}
        />
      </React.Fragment>
    );
  }

  return <group>{lines}</group>;
}

/* ====================== CAMERA CONTROLLER ======================= */
const CameraController = forwardRef(function CameraController(
  { controlsRef },
  ref
) {
  const { camera } = useThree();

  useImperativeHandle(ref, () => ({
    setCameraPreset(name) {
      if (name === "front") camera.position.set(0, 1.2, 4.5);
      if (name === "iso") camera.position.set(3, 2, 3);
      camera.lookAt(0, 1, 0);
      controlsRef.current?.update();
    },
    resetCamera() {
      camera.position.set(4, 2, 5);
      camera.lookAt(0, 1, 0);
      controlsRef.current?.update();
    },
  }));

  return null;
});

/* =========================== SCENE ============================== */
const SceneCanvas = forwardRef(function SceneCanvas(_, ref) {
  const controlsRef = useRef(null);
  const cameraRef = useRef(null);

  // 🔒 Defensive selector (prevents transient undefined crashes)
  const modelUrl = useModelStore(
    (s) => s?.currentModelUrl ?? null
  );

  useImperativeHandle(ref, () => ({
    setCameraPreset: (name) =>
      cameraRef.current?.setCameraPreset(name),
    resetCamera: () =>
      cameraRef.current?.resetCamera(),
  }));

  return (
    <div className="relative w-full h-[520px] bg-slate-50">
      <Canvas
        shadows
        dpr={[1, 2]}
        gl={{ antialias: true }}
        camera={{ position: [4, 2, 5], fov: 38 }}
      >
        <color attach="background" args={["#f6f8fb"]} />

        <ambientLight intensity={0.6} />
        <directionalLight position={[5, 8, 5]} intensity={1.1} />

        <WireGrid />

        <Suspense fallback={null}>
          {modelUrl ? (
            <ModelLoader url={modelUrl} />
          ) : (
            <mesh position={[0, 1, 0]}>
              <boxGeometry args={[1, 1, 1]} />
              <meshStandardMaterial
                color="#d9dee3"
                roughness={0.5}
                metalness={0.1}
              />
            </mesh>
          )}
        </Suspense>

        <OrbitControls ref={controlsRef} />
        <CameraController
          ref={cameraRef}
          controlsRef={controlsRef}
        />
      </Canvas>
    </div>
  );
});

export default SceneCanvas;

