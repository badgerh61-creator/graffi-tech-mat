// src/engine/SceneCanvas.jsx
import React, {
  forwardRef,
  useRef,
  useImperativeHandle,
  Suspense,
  useMemo,
} from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, Environment, Line } from "@react-three/drei";
import { useModelStore } from "../store/modelStore";
import ModelLoader from "./ModelLoader";

/* -------------------------- GRID FLOOR -------------------------- */
function WireGrid() {
  const size = 30;
  const divisions = 30;

  const lines = [];
  for (let i = -divisions; i <= divisions; i++) {
    const pos = (i * size) / divisions; 
    const fade = 0.15 + (0.85 * (divisions - Math.abs(i))) / divisions;

    lines.push(
      <Line
        key={"v-" + i}
        points={[
          [pos, 0, -size],
          [pos, 0, size],
        ]}
        color={`rgba(64,88,125,${fade})`}
        lineWidth={1}
      />,
      <Line
        key={"h-" + i}
        points={[
          [-size, 0, pos],
          [size, 0, pos],
        ]}
        color={`rgba(64,88,125,${fade})`}
        lineWidth={1}
      />
    );
  }

  return <group position={[0,0,0]}>{lines}</group>;
}

/* -------------------------- CAMERA CONTROLLER -------------------------- */
const CameraController = forwardRef(function CameraController(
  { controlsRef },
  ref
) {
  const { camera } = useThree();

  useImperativeHandle(ref, () => ({
    setCameraPreset: (name) => {
      if (name === "front") {
        camera.position.set(0, 1.2, 4.5);
      } else if (name === "iso") {
        camera.position.set(3, 2, 3);
      }
      camera.lookAt(0, 1, 0);
      controlsRef.current?.update();
    },
    resetCamera: () => {
      camera.position.set(4, 2, 5);
      camera.lookAt(0, 1, 0);
      controlsRef.current?.update();
    },
  }));

  return null;
});

/* ------------------------------ MAIN SCENE ------------------------------ */
const SceneCanvas = forwardRef(function SceneCanvas({ onDragState }, ref) {
  const controlsRef = useRef();
  const cameraRef = useRef();

  const modelId = useModelStore((s) => s.currentModelId);
  const models = useModelStore((s) => s.models);

  const currentModel = useMemo(
    () => models.find((m) => m.id === modelId) || null,
    [models, modelId]
  );

  useImperativeHandle(ref, () => ({
    setCameraPreset: (name) => cameraRef.current?.setCameraPreset(name),
    resetCamera: () => cameraRef.current?.resetCamera(),
  }));

  return (
    <div style={{ width: "100%", height: "520px" }}>
      <Canvas
        shadows
        camera={{ position: [4, 2, 5], fov: 38 }}
        onPointerDown={() => onDragState?.(true)}
        onPointerUp={() => onDragState?.(false)}
        className="r3f-canvas"
      >
        <color attach="background" args={["#f6f8fb"]} />
        <ambientLight intensity={0.6} />
        <directionalLight
          castShadow
          intensity={1.1}
          position={[5, 8, 5]}
        />

        <WireGrid />

        <Suspense fallback={null}>
          {currentModel ? (
            <ModelLoader url={currentModel.url} />
          ) : (
            <mesh position={[0, 1, 0]} castShadow receiveShadow>
              <boxGeometry args={[1, 1, 1]} />
              <meshStandardMaterial color="#d9dee3" roughness={0.5} />
            </mesh>
          )}
        </Suspense>

        <Environment preset="studio" />
        <OrbitControls ref={controlsRef} />
        <CameraController ref={cameraRef} controlsRef={controlsRef} />
      </Canvas>
    </div>
  );
});

export default SceneCanvas;
