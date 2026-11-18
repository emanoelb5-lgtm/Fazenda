import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { validateScene } from './scene-data.js';
import './style.css';

const $ = id => document.getElementById(id);
const host = $('canvas-host');
const viewport = $('viewport');
const overlay = $('loading-overlay');
const status = $('live-status');
const base = import.meta.env.BASE_URL;
let renderer, camera, controls, scene, frame, model, sceneData, bounds;
let ready = false;
let rendererMode = 'webgl';
let view = 'orbit';
let toastTimer;

function toast(message) {
  $('toast').textContent = message;
  $('toast').classList.add('visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $('toast').classList.remove('visible'), 3600);
}

function showError(message) {
  ready = false;
  overlay.hidden = false;
  overlay.querySelector('strong').textContent = 'O cenário ainda não abriu';
  overlay.querySelector('span').textContent = message;
  $('retry').hidden = false;
  status.innerHTML = '<i></i>INDISPONÍVEL';
}

function selectView(value) {
  view = value;
  for (const [id, name] of [['orbit-view', 'orbit'], ['top-view', 'top']]) {
    $(id).classList.toggle('selected', value === name);
    $(id).setAttribute('aria-pressed', String(value === name));
  }
}

function fitCamera(mode = 'orbit') {
  if (!ready) return;
  selectView(mode);
  const direction = mode === 'top' ? new THREE.Vector3(0.001, 1, 0.001).normalize() : new THREE.Vector3(1.05, 0.88, 1.2).normalize();
  const center = bounds.getCenter(new THREE.Vector3());
  center.y = mode === 'top' ? 0 : 1.7;
  controls.target.copy(center);
  const corners = [];
  for (const x of [bounds.min.x, bounds.max.x]) for (const y of [bounds.min.y, bounds.max.y]) for (const z of [bounds.min.z, bounds.max.z]) corners.push(new THREE.Vector3(x, y, z));
  let low = 10, high = 180;
  for (let i = 0; i < 28; i++) {
    const distance = (low + high) / 2;
    camera.position.copy(center).addScaledVector(direction, distance);
    camera.lookAt(center);
    camera.updateMatrixWorld();
    const fits = corners.every(corner => {
      const p = corner.clone().project(camera);
      return Math.abs(p.x) < 0.85 && Math.abs(p.y) < 0.79 && p.z < 1;
    });
    if (fits) high = distance;
    else low = distance;
  }
  camera.position.copy(center).addScaledVector(direction, high);
  controls.update();
  render();
}

function updateScale() {
  if (!ready) return;
  const point = controls.target.clone();
  const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
  const from = point.clone().project(camera);
  const to = point.addScaledVector(right, 10).project(camera);
  const pixels = Math.abs(to.x - from.x) * host.clientWidth / 2;
  const length = pixels > 130 ? 5 : 10;
  const scale = document.querySelector('.scale');
  scale.lastChild.textContent = `${length} m`;
  scale.querySelector('i').style.width = `${Math.max(4, pixels * length / 10)}px`;
  const angle = controls.getAzimuthalAngle() * 180 / Math.PI;
  $('compass-arrow').style.transform = `rotate(${-angle}deg)`;
}

function render() {
  if (!renderer || !scene || !camera) return;
  renderer.render(scene, camera);
  updateScale();
}

function resize() {
  if (!renderer || !camera) return;
  const width = host.clientWidth;
  const height = host.clientHeight;
  if (!width || !height) return;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  render();
}

async function init() {
  try {
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
    } catch {
      const { SVGRenderer } = await import('three/addons/renderers/SVGRenderer.js');
      renderer = new SVGRenderer();
      renderer.setQuality('low');
      renderer.setPrecision(2);
      renderer.setClearColor(0xdce5d1);
      rendererMode = 'svg';
      host.classList.add('compatibility-mode');
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.8));
    if (renderer.shadowMap) {
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    host.appendChild(renderer.domElement);
    renderer.domElement.addEventListener('webglcontextlost', event => {
      event.preventDefault();
      showError('O navegador interrompeu a visualização 3D. Toque em tentar novamente.');
    });
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(40, 1, 0.1, 500);
    camera.position.set(45, 36, 45);
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = rendererMode === 'webgl';
    controls.dampingFactor = 0.12;
    controls.minDistance = 8;
    controls.maxDistance = 180;
    controls.minPolarAngle = 0.003;
    controls.maxPolarAngle = Math.PI / 2 - 0.045;
    controls.maxTargetRadius = 28;
    controls.screenSpacePanning = true;
    controls.touches.ONE = THREE.TOUCH.ROTATE;
    controls.touches.TWO = THREE.TOUCH.DOLLY_PAN;
    controls.addEventListener('change', render);
    scene.add(new THREE.HemisphereLight(0xf9ffed, 0x718553, 2.8));
    const sun = new THREE.DirectionalLight(0xfff4d6, 3.4);
    sun.position.set(-18, 32, 14);
    sun.castShadow = true;
    sun.shadow.mapSize.set(1024, 1024);
    Object.assign(sun.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30, near: 1, far: 100 });
    sun.shadow.normalBias = 0.04;
    sun.shadow.bias = -0.0003;
    sun.shadow.camera.updateProjectionMatrix();
    scene.add(sun);
    const shadow = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.ShadowMaterial({ opacity: 0.10 }));
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = -1.46;
    shadow.receiveShadow = true;
    if (rendererMode === 'webgl') scene.add(shadow);
    resize();
    new ResizeObserver(resize).observe(host);
    const [response, gltf] = await Promise.all([
      fetch(`${base}data/fazenda.scene.json`),
      new GLTFLoader().loadAsync(`${base}models/fazenda-fase0.glb`),
    ]);
    if (!response.ok) throw new Error('Não foi possível carregar os dados da cena.');
    sceneData = validateScene(await response.json());
    model = gltf.scene;
    let triangles = 0;
    model.traverse(object => {
      if (!object.isMesh) return;
      if (rendererMode === 'svg') {
        if (object.name.includes('Cobertura')) object.visible = false;
        const simplified = original => new THREE.MeshBasicMaterial({ color: original.color, side: original.side });
        object.material = Array.isArray(object.material) ? object.material.map(simplified) : simplified(object.material);
      }
      object.castShadow = true;
      object.receiveShadow = true;
      triangles += (object.geometry.index?.count || object.geometry.attributes.position.count) / 3;
    });
    const ids = new Set();
    model.traverse(object => { if (object.userData.instance_id) ids.add(object.userData.instance_id); });
    if (!ids.has(sceneData.terrain.instance_id) || !sceneData.instances.every(instance => ids.has(instance.instance_id))) throw new Error('O modelo não corresponde à cena de referência.');
    scene.add(model);
    bounds = new THREE.Box3().setFromObject(model);
    ready = true;
    host.dataset.renderer = rendererMode;
    host.dataset.ready = 'true';
    overlay.hidden = true;
    status.innerHTML = rendererMode === 'webgl' ? '<i></i>PRONTO PARA EXPLORAR' : '<i></i>VISUAL SIMPLIFICADO';
    if (rendererMode === 'svg') toast('Visual simplificado: este navegador está com os gráficos 3D desativados.');
    fitCamera();
    // Read-only diagnostics for reproducible QA; no credentials or user records.
    window.fazendaDiagnostics = () => ({ ready, view, renderer: rendererMode, triangles, objects: ids.size, units: sceneData.units,
      terrain: sceneData.terrain.size, camera: camera.position.toArray(), target: controls.target.toArray(),
      drawCalls: renderer.info?.render?.calls ?? null });
    const animate = () => {
      frame = requestAnimationFrame(animate);
      if (!document.hidden) controls.update();
    };
    animate();
  } catch (error) {
    console.error('Falha ao abrir a fazenda:', error);
    showError('Confira sua conexão e se este navegador permite gráficos 3D. Os arquivos do cenário continuam disponíveis abaixo.');
  }
}

function zoom(factor) {
  if (!ready) return;
  const offset = camera.position.clone().sub(controls.target);
  offset.setLength(THREE.MathUtils.clamp(offset.length() * factor, controls.minDistance, controls.maxDistance));
  camera.position.copy(controls.target).add(offset);
  controls.update();
  render();
}

$('orbit-view').addEventListener('click', () => fitCamera('orbit'));
$('top-view').addEventListener('click', () => fitCamera('top'));
$('reset-view').addEventListener('click', () => fitCamera('orbit'));
$('zoom-in').addEventListener('click', () => zoom(0.8));
$('zoom-out').addEventListener('click', () => zoom(1.25));
$('retry').addEventListener('click', () => location.reload());
$('help-button').addEventListener('click', () => $('help-dialog').showModal());
$('close-help').addEventListener('click', () => $('help-dialog').close());
$('help-dialog').addEventListener('click', event => { if (event.target === $('help-dialog')) $('help-dialog').close(); });
$('fullscreen').addEventListener('click', async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else if (viewport.requestFullscreen) await viewport.requestFullscreen();
    else toast('Gire o celular para aproveitar uma vista maior.');
  } catch { toast('Seu navegador não liberou a tela cheia. Tente girar o celular.'); }
});
document.addEventListener('fullscreenchange', () => {
  requestAnimationFrame(() => { resize(); if (ready) fitCamera(view); });
  $('fullscreen').setAttribute('aria-label', document.fullscreenElement ? 'Sair da tela cheia' : 'Tela cheia');
});
window.addEventListener('pagehide', event => { if (!event.persisted) cancelAnimationFrame(frame); });
init();
