import { test, expect } from '@playwright/test';



test('Поиск на Википедии работает корректно', async ({ page }) => {
  await page.goto('https://www.wikipedia.org/');

  await page.fill('#searchInput', 'Python');
  await page.keyboard.press('Enter');

  await expect(page.locator('#firstHeading')).toContainText('Python');
});


test('Переключение языка на русский', async ({ page }) => {
  await page.goto('https://www.wikipedia.org/');

  await page.click('#js-link-box-ru');

  await expect(page).toHaveURL(/ru.wikipedia.org/);
});


test('Проверка валидации формы', async ({ page }) => {
  await page.goto('https://www.selenium.dev/selenium/web/web-form.html');

  await page.click('button');

  const input = page.locator('#my-text-id');
  await expect(input).toHaveValue('');
});


test('Редирект после действия', async ({ page }) => {
  const response = await page.request.get('https://httpbin.org/redirect/1');
  expect(response.status()).toBe(302);

  const final = await page.request.get('https://httpbin.org/get');
  expect(final.status()).toBe(200);
});


test('Успешная авторизация через API', async ({ request }) => {
  const response = await request.post('https://reqres.in/api/login', {
    data: {
      email: 'eve.holt@reqres.in',
      password: 'cityslicka'
    }
  });

  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body.token).toBeTruthy();
});


test('Ошибка при неверных данных', async ({ request }) => {
  const response = await request.post('https://reqres.in/api/login', {
    data: {
      email: 'wrong@example.com',
      password: '123'
    }
  });

  expect(response.status()).toBe(400);
  const body = await response.json();
  expect(body.error).toBe('user not found');
});



test('Проверка API через network-подход', async ({ page }) => {
  const [request] = await Promise.all([
    page.waitForRequest(req => req.url().includes('/api/users')),
    page.goto('https://reqres.in/api/users?page=2')
  ]);

  expect(request.method()).toBe('GET');
});
