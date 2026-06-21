const container = document.getElementById('viewer-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x000000, 0);
container.appendChild(renderer.domElement);

// Lighting
scene.add(new THREE.AmbientLight(0xffffff, 0.7));
const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
dirLight.position.set(100, 200, 150);
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
fillLight.position.set(-100, 50, -100);
scene.add(fillLight);

// Controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.0;
controls.enablePan = false;
controls.enableZoom = false;

// Store reference to blaster meshes
let blasterMeshes = [];

// Load OBJ
const loader = new THREE.OBJLoader();
loader.load('blaster.obj', function(obj) {
    obj.traverse(function(child) {
        if (child.isMesh) {
            child.material = new THREE.MeshStandardMaterial({
                color: 0x555555,
                metalness: 0.7,
                roughness: 0.3
            });
            blasterMeshes.push(child);
        }
    });

    // Rotate blaster 90 degrees to point north (up)
    obj.rotation.x = -Math.PI / 2;

    // Center model at origin
    const box = new THREE.Box3().setFromObject(obj);
    const center = box.getCenter(new THREE.Vector3());
    obj.position.sub(center);

    scene.add(obj);

    // Recalculate bounding after centering
    const newBox = new THREE.Box3().setFromObject(obj);
    const size = newBox.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    const dist = maxDim / (2 * Math.tan(fov / 2));

    camera.position.set(0, 0, dist * 1.1);
    camera.near = dist / 100;
    camera.far = dist * 10;
    camera.updateProjectionMatrix();

    controls.target.set(0, 0, 0);
    controls.update();
}, undefined, function(err) {
    console.error('Error loading OBJ:', err);
});

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// Resize
window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});

// Color picker
document.querySelectorAll('.color-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const color = parseInt(btn.dataset.color);
        blasterMeshes.forEach(mesh => {
            mesh.material.color.setHex(color);
        });
        document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});
// Set first button as active
document.querySelector('.color-btn').classList.add('active');
