import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Stars, MeshDistortMaterial, Text } from '@react-three/drei';
import { motion } from 'framer-motion';
import './App.css';

function HeroGeometry() {
  const meshRef = useRef();
  const [hovered, setHover] = useState(false);

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    if (meshRef.current) {
      meshRef.current.rotation.x = t * 0.2;
      meshRef.current.rotation.y = t * 0.3;
    }
  });

  return (
    <Float speed={2} rotationIntensity={1.5} floatIntensity={2}>
      <mesh 
        ref={meshRef}
        scale={hovered ? 2.8 : 2.5}
        onPointerOver={() => setHover(true)}
        onPointerOut={() => setHover(false)}
        position={[2, 0, 0]}
      >
        <icosahedronGeometry args={[1, 15]} />
        <MeshDistortMaterial
          color={hovered ? "#00c6ff" : "#202020"}
          emissive={hovered ? "#0072ff" : "#000000"}
          roughness={0.1}
          metalness={1}
          distort={0.4}
          speed={2}
          wireframe={true}
        />
      </mesh>
    </Float>
  );
}

function FloatingText() {
  return (
    <Float speed={1.5} rotationIntensity={0.5} floatIntensity={0.5}>
       <Text
        fontSize={0.5}
        color="#333"
        position={[2, -2.5, 0]}
        anchorX="center"
        anchorY="middle"
      >
        &lt;/&gt;
      </Text>
    </Float>
  );
}

function App() {
  return (
    <>
      <div id="canvas-container">
        <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
          <color attach="background" args={['#050505']} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} color="#00c6ff"/>
          <pointLight position={[-10, -10, -10]} intensity={0.5} color="#ff0072"/>
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          <HeroGeometry />
          <FloatingText />
        </Canvas>
      </div>

      <div className="overlay">
        <motion.div 
          className="content-block"
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1, ease: "easeOut" }}
        >
          <h4>WEB DEVELOPER STUDENT</h4>
          <h1>ARYAN SHAKYA</h1>
          <p>
            Building immersive web experiences with modern technologies.
            Specializing in React, 3D WebGL interactions, and creative frontend development.
          </p>
          <motion.button 
            className="btn"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            View My Projects
          </motion.button>
        </motion.div>
      </div>
    </>
  );
}

export default App;