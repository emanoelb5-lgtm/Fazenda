import { test, expect } from '@playwright/test';

test('carrega o GLB com WebGL, navega e mantém o layout dentro da tela', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  const host = page.locator('#canvas-host');
  await expect(host).toHaveAttribute('data-ready', 'true');
  await expect(host).toHaveAttribute('data-renderer', 'webgl');
  const initial = await page.evaluate(() => window.fazendaDiagnostics());
  expect(initial.objects).toBe(2);
  expect(initial.terrain).toEqual([40, 40]);
  expect(initial.triangles).toBeGreaterThan(5000);
  await page.getByRole('button', { name: 'Aproximar', exact: true }).click();
  const zoomed = await page.evaluate(() => window.fazendaDiagnostics());
  const distance = s => Math.hypot(...s.camera.map((value, i) => value - s.target[i]));
  expect(distance(zoomed)).toBeLessThan(distance(initial));
  await page.locator('#top-view').click();
  await expect(page.locator('#top-view')).toHaveAttribute('aria-pressed', 'true');
  expect((await page.evaluate(() => window.fazendaDiagnostics())).view).toBe('top');
  await page.getByRole('button', { name: 'Voltar à vista inicial', exact: true }).click();
  expect((await page.evaluate(() => window.fazendaDiagnostics())).view).toBe('orbit');
  await page.getByRole('button', { name: 'Como navegar', exact: true }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('button', { name: 'Fechar ajuda', exact: true }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  expect(errors).toEqual([]);
});

test('os downloads contêm os arquivos reais', async ({ request }) => {
  const model = await request.get('/models/fazenda-fase0.glb');
  expect(model.ok()).toBe(true);
  expect((await model.body()).subarray(0, 4).toString()).toBe('glTF');
  const render = await request.get('/renders/fase0.png');
  expect(render.ok()).toBe(true);
  expect(render.headers()['content-type']).toContain('image/png');
  const data = await request.get('/data/fazenda.scene.json');
  expect((await data.json()).scene_id).toBe('fazenda-fase-0');
});
