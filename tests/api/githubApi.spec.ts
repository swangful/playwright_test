import { expect, test } from '@playwright/test';

function assertJsonHeaders(headers: { [p: string]: string }) {
  expect(headers['content-type'] ?? headers['Content-Type']).toMatch(/^application\/json/);
  const lower = Object.fromEntries(
    Object.entries(headers).map(([k, v]) => [k.toLowerCase(), v]),
  );
  expect(lower).toHaveProperty('x-ratelimit-limit');
  expect(lower).toHaveProperty('x-ratelimit-remaining');
}

test.describe('GitHub /users', () => {
  for (const login of ['swangful', 'octocat']) {
    test(`GET /users/${login} — success`, async ({ request }) => {
      const response = await request.get(`/users/${login}`);
      expect(response.status()).toBe(200);
      assertJsonHeaders(response.headers());
      const body = (await response.json()) as Record<string, unknown>;
      expect(String(body.login).toLowerCase()).toBe(login.toLowerCase());
      expect(typeof body.id).toBe('number');
      expect(body.type).toBe('User');
      expect(typeof body.public_repos).toBe('number');
    });
  }

  test('GET /users/{unknown} — 404', async ({ request }) => {
    const response = await request.get('/users/this-login-should-not-exist-404-xyz');
    expect(response.status()).toBe(404);
    assertJsonHeaders(response.headers());
    const body = (await response.json()) as { message?: string };
    expect(body).toHaveProperty('message');
  });

  test('GET /users with invalid login — 404', async ({ request }) => {
    const response = await request.get('/users/!!!not-a-valid-login!!!');
    expect(response.status()).toBe(404);
  });

  test('response headers include request id and JSON content-type', async ({ request }) => {
    const response = await request.get('/users/octocat');
    expect(response.status()).toBe(200);
    const lower = Object.fromEntries(
      Object.entries(response.headers()).map(([k, v]) => [k.toLowerCase(), v]),
    );
    expect(lower['content-type']).toMatch(/^application\/json/);
    expect(lower['x-github-request-id']).toBeTruthy();
  });

  test('ETag supports conditional GET (304)', async ({ request }, testInfo) => {
    const first = await request.get('/users/octocat');
    expect(first.status()).toBe(200);
    const etag = first.headers()['etag'] ?? first.headers()['ETag'];
    if (!etag) {
      testInfo.skip();
      return;
    }
    const second = await request.get('/users/octocat', {
      headers: { 'If-None-Match': etag },
    });
    expect(second.status()).toBe(304);
  });
});

test.describe('GitHub /search/users', () => {
  test('finds swangful', async ({ request }) => {
    const response = await request.get('/search/users', { params: { q: 'swangful' } });
    expect(response.status()).toBe(200);
    assertJsonHeaders(response.headers());
    const body = (await response.json()) as { items: { login: string }[] };
    expect(Array.isArray(body.items)).toBeTruthy();
    const logins = new Set(body.items.map((i) => i.login.toLowerCase()));
    expect(logins.has('swangful')).toBeTruthy();
  });

  test('empty q — 422', async ({ request }) => {
    const response = await request.get('/search/users', { params: { q: '' } });
    expect(response.status()).toBe(422);
    const body = (await response.json()) as { message?: string };
    expect(body).toHaveProperty('message');
  });

  test('broad query — 200 or 403 (rate limit)', async ({ request }) => {
    const response = await request.get('/search/users', {
      params: { q: 'location:San Francisco' },
    });
    expect([200, 403]).toContain(response.status());
    if (response.status() === 200) {
      assertJsonHeaders(response.headers());
      const body = (await response.json()) as { total_count?: number };
      expect(body).toHaveProperty('total_count');
    }
  });
});

test.describe('GitHub /users/{login}/repos', () => {
  test('list length matches public_repos for swangful', async ({ request }) => {
    const user = await request.get('/users/swangful');
    expect(user.status()).toBe(200);
    const { public_repos: expected } = (await user.json()) as { public_repos: number };

    const repos = await request.get('/users/swangful/repos', {
      params: { per_page: '100', type: 'owner' },
    });
    expect(repos.status()).toBe(200);
    expect(repos.headers()['content-type']).toMatch(/^application\/json/);
    const data = (await repos.json()) as unknown[];
    expect(Array.isArray(data)).toBeTruthy();
    expect(data.length).toBe(expected);
  });

  test('repo objects include expected keys', async ({ request }) => {
    const response = await request.get('/users/swangful/repos', { params: { per_page: '5' } });
    expect(response.status()).toBe(200);
    const data = (await response.json()) as Record<string, unknown>[];
    expect(data.length).toBeGreaterThanOrEqual(1);
    const repo = data[0];
    for (const key of ['name', 'full_name', 'html_url', 'private', 'stargazers_count']) {
      expect(repo).toHaveProperty(key);
    }
  });

  test('unknown user — 404', async ({ request }) => {
    const response = await request.get(
      '/users/this-login-should-not-exist-404-xyz/repos',
    );
    expect(response.status()).toBe(404);
  });

  test('accepts sort and direction', async ({ request }) => {
    const response = await request.get('/users/swangful/repos', {
      params: { per_page: '5', sort: 'updated', direction: 'desc' },
    });
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toMatch(/^application\/json/);
    const data = (await response.json()) as unknown[];
    expect(Array.isArray(data)).toBeTruthy();
  });
});
