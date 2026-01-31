// Import Three.js from a standard CDN
import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';

// 1. Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.getElementById('canvas-container').appendChild(renderer.domElement);

// 2. The "Hero" Object (Wireframe Icosahedron)
const geometry = new THREE.IcosahedronGeometry(1.5, 1);
const material = new THREE.MeshBasicMaterial({ 
    color: 0x00c6ff,
    wireframe: true,
    transparent: true,
    opacity: 0.5
});
const heroMesh = new THREE.Mesh(geometry, material);
heroMesh.position.set(2, 0, 0); // Move to the right side
scene.add(heroMesh);

// 3. Starfield Background
const starGeometry = new THREE.BufferGeometry();
const starCount = 2000;
const posArray = new Float32Array(starCount * 3);

for(let i = 0; i < starCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 50; // Random spread
}

starGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const starMaterial = new THREE.PointsMaterial({
    size: 0.05,
    color: 0xffffff,
    transparent: true,
    opacity: 0.8
});
const stars = new THREE.Points(starGeometry, starMaterial);
scene.add(stars);

// 4. Lighting (Subtle)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Camera Position
camera.position.z = 5;

// 5. Interaction (Mouse Movement)
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX / window.innerWidth - 0.5;
    mouseY = event.clientY / window.innerHeight - 0.5;
});

// 6. Animation Loop
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const elapsedTime = clock.getElapsedTime();

    // Rotate the Hero Mesh
    heroMesh.rotation.y += 0.005;
    heroMesh.rotation.x += 0.002;
    
    // "Breathing" scale effect
    const scale = 1 + Math.sin(elapsedTime) * 0.05;
    heroMesh.scale.set(scale, scale, scale);

    // Rotate Stars slightly
    stars.rotation.y += 0.0005;

    // Parallax Effect (Scene moves slightly with mouse)
    camera.position.x += (mouseX * 0.5 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 0.5 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
}

// 7. Handle Window Resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    // Responsive: Move mesh to center on mobile, right on desktop
    if(window.innerWidth < 768) {
        heroMesh.position.set(0, 0, 0);
    } else {
        heroMesh.position.set(2, 0, 0);
    }
});

// Initial check for mobile layout
if(window.innerWidth < 768) {
    heroMesh.position.set(0, 0, 0);
}

animate();