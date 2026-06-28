import "./styles.css";
import * as THREE from "three";

const root = document.querySelector<HTMLDivElement>("#app");

if (!root) {
  throw new Error("Missing #app");
}

const appRoot = root;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101412);

const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(2.5, 2, 4);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
appRoot.appendChild(renderer.domElement);

const light = new THREE.DirectionalLight(0xffffff, 2);
light.position.set(3, 4, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x8fb6a0, 0.8));

const geometry = new THREE.IcosahedronGeometry(1, 1);
const material = new THREE.MeshStandardMaterial({
  color: 0x70d6a4,
  roughness: 0.45,
  metalness: 0.05
});
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

function resize(): void {
  const width = appRoot.clientWidth;
  const height = appRoot.clientHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height, false);
}

function animate(): void {
  mesh.rotation.x += 0.005;
  mesh.rotation.y += 0.008;
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

window.addEventListener("resize", resize);
resize();
animate();
