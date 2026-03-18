// ═══════════════════════════════════════════════════
//  HERO — Three.js Wireframe + Orbital Scene (GMX style)
// ═══════════════════════════════════════════════════
(function () {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  const W = () => window.innerWidth;
  const H = () => window.innerHeight;

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(W(), H());
  renderer.setClearColor(0x000000, 0);

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, W() / H(), 0.1, 1000);
  camera.position.set(0, 0, 5);

  // ── Mouse ──────────────────────────────────────────
  const mouse = { x: 0, y: 0 };
  window.addEventListener('mousemove', e => {
    mouse.x = (e.clientX / W() - 0.5) * 2;
    mouse.y = (e.clientY / H() - 0.5) * 2;
  });

  // ── Central Wireframe Icosahedron ──────────────────
  const icoGeo = new THREE.IcosahedronGeometry(1.5, 1);
  const icoMat = new THREE.MeshBasicMaterial({
    color: 0xc8ff00,   // lime accent
    wireframe: true,
    transparent: true,
    opacity: 0.22,
  });
  const ico = new THREE.Mesh(icoGeo, icoMat);
  ico.position.set(1.8, 0, 0);
  scene.add(ico);

  // Inner solid (faint)
  const innerGeo = new THREE.IcosahedronGeometry(1.35, 1);
  const innerMat = new THREE.MeshBasicMaterial({
    color: 0xffffff, wireframe: true, transparent: true, opacity: 0.04
  });
  const inner = new THREE.Mesh(innerGeo, innerMat);
  inner.position.copy(ico.position);
  scene.add(inner);

  // ── Orbital rings ──────────────────────────────────
  function makeRing(radius, color, opacity, tilt) {
    const geo = new THREE.TorusGeometry(radius, 0.004, 4, 120);
    const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity });
    const m   = new THREE.Mesh(geo, mat);
    m.rotation.x = tilt[0];
    m.rotation.y = tilt[1];
    m.position.copy(ico.position);
    scene.add(m);
    return m;
  }
  const ring1 = makeRing(2.2, 0xc8ff00, 0.3, [Math.PI / 2, 0]);
  const ring2 = makeRing(2.5, 0xffffff, 0.12, [Math.PI / 3, 0.4]);
  const ring3 = makeRing(2.8, 0xc8ff00, 0.07, [Math.PI / 4, -0.6]);

  // ── Star field ────────────────────────────────────
  const starCount = 1800;
  const starPos   = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    const i3 = i * 3;
    starPos[i3]     = (Math.random() - 0.5) * 40;
    starPos[i3 + 1] = (Math.random() - 0.5) * 40;
    starPos[i3 + 2] = (Math.random() - 0.5) * 40 - 5;
  }
  const starGeo = new THREE.BufferGeometry();
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.025, transparent: true, opacity: 0.5 });
  scene.add(new THREE.Points(starGeo, starMat));

  // ── Floating particles (lime + white) ─────────────
  const PTS = 600;
  const pPos = new Float32Array(PTS * 3);
  for (let i = 0; i < PTS; i++) {
    const i3 = i * 3;
    const r  = 3.5 + Math.random() * 4;
    const t  = Math.random() * Math.PI * 2;
    const p  = Math.acos(2 * Math.random() - 1);
    pPos[i3]     = r * Math.sin(p) * Math.cos(t) + ico.position.x;
    pPos[i3 + 1] = r * Math.sin(p) * Math.sin(t);
    pPos[i3 + 2] = r * Math.cos(p);
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  const pMat = new THREE.PointsMaterial({ color: 0xc8ff00, size: 0.04, transparent: true, opacity: 0.6 });
  scene.add(new THREE.Points(pGeo, pMat));

  // ── Animation ────────────────────────────────────
  const clock = new THREE.Clock();
  let mx = 0, my = 0;

  function animate() {
    requestAnimationFrame(animate);
    const t  = clock.getElapsedTime();
    mx += (mouse.x - mx) * 0.04;
    my += (mouse.y - my) * 0.04;

    ico.rotation.x   = t * 0.1 + my * 0.15;
    ico.rotation.y   = t * 0.15 + mx * 0.15;
    inner.rotation.x = -t * 0.08 + my * 0.1;
    inner.rotation.y = -t * 0.12 + mx * 0.1;

    ring1.rotation.z = t * 0.18;
    ring2.rotation.z = -t * 0.12;
    ring3.rotation.y = t * 0.08;
    ring3.rotation.z = t * 0.06;

    camera.position.x += (mx * 0.25 - camera.position.x) * 0.05;
    camera.position.y += (-my * 0.18 - camera.position.y) * 0.05;
    camera.lookAt(ico.position);

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = W() / H();
    camera.updateProjectionMatrix();
    renderer.setSize(W(), H());
  });
})();
