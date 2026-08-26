/**
 * @jest-environment jsdom
 *
 * Offline Sync / PWA contract tests.
 * Runner target: Vitest or Jest with jsdom.
 *
 * The repository currently has no package.json or frontend test runner, so this
 * file is the QA acceptance suite to enable when the runner is added.
 */

const SYNC_ENDPOINT = "/api/sync/batch";

function setOnlineState(value) {
  Object.defineProperty(navigator, "onLine", {
    configurable: true,
    get: () => value,
  });
}

function makeOperation(overrides = {}) {
  return {
    operation_id: "op-front-sync-001",
    entity_type: "PERSONA",
    entity_id: "p-front-sync-001",
    operation_type: "CREATE",
    payload: { estado: "estoy_bien", version: 1 },
    client_created_at: "2026-08-24T12:00:00Z",
    ...overrides,
  };
}

function createSyncHarness({ queue = [], fetchImpl = jest.fn(), online = true } = {}) {
  setOnlineState(online);

  const localDb = {
    readQueue: jest.fn(async () => [...queue]),
    clearQueue: jest.fn(async () => {
      queue.length = 0;
    }),
    replaceQueue: jest.fn(async (nextQueue) => {
      queue.length = 0;
      queue.push(...nextQueue);
    }),
  };

  const renderStatus = (state, message) => {
    document.body.innerHTML = `
      <section data-testid="sync-status" data-state="${state}">
        ${message}
      </section>
    `;
  };

  const processPendingQueue = async () => {
    const pending = await localDb.readQueue();

    if (pending.length === 0) {
      renderStatus("empty", "Todo sincronizado / No hay cambios pendientes");
      return { synced: 0, retained: 0 };
    }

    if (!navigator.onLine) {
      renderStatus("error", "Sin conexion. Los cambios se sincronizaran mas tarde.");
      return { synced: 0, retained: pending.length };
    }

    renderStatus("loading", "Sincronizando datos pendientes...");

    try {
      const response = await fetchImpl(SYNC_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ operations: pending }),
      });

      if (!response.ok) {
        throw new Error(`Sync failed with ${response.status}`);
      }

      const body = await response.json();
      const retainedStatuses = new Set(["CONFLICT", "INVALID", "RETRYABLE_ERROR"]);
      const retained = pending.filter((operation) => {
        const result = body.results.find(
          (item) => item.operation_id === operation.operation_id,
        );
        return !result || retainedStatuses.has(result.status);
      });

      if (retained.length > 0) {
        await localDb.replaceQueue(retained);
        renderStatus("error", "Algunos cambios no se han sincronizado.");
        return { synced: pending.length - retained.length, retained: retained.length };
      }

      await localDb.clearQueue();
      renderStatus("empty", "Todo sincronizado / No hay cambios pendientes");
      return { synced: pending.length, retained: 0 };
    } catch (error) {
      await localDb.replaceQueue(pending);
      renderStatus("error", "No se pudieron sincronizar los datos pendientes.");
      return { synced: 0, retained: pending.length };
    }
  };

  return { localDb, processPendingQueue, queue };
}

describe("Offline Sync / PWA queue", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    jest.restoreAllMocks();
  });

  test("Carga: muestra indicador mientras sincroniza datos pendientes", async () => {
    let resolveFetch;
    const fetchImpl = jest.fn(
      () =>
        new Promise((resolve) => {
          resolveFetch = resolve;
        }),
    );
    const { processPendingQueue } = createSyncHarness({
      queue: [makeOperation()],
      fetchImpl,
    });

    const syncPromise = processPendingQueue();

    expect(document.body.textContent).toContain("Sincronizando datos pendientes...");
    expect(document.querySelector("[data-testid='sync-status']").dataset.state).toBe("loading");

    resolveFetch({
      ok: true,
      status: 200,
      json: async () => ({
        results: [{ operation_id: "op-front-sync-001", status: "APPLIED" }],
      }),
    });
    await syncPromise;
  });

  test("Vacio: no llama al backend si no hay cambios pendientes", async () => {
    const fetchImpl = jest.fn();
    const { processPendingQueue } = createSyncHarness({ queue: [], fetchImpl });

    const result = await processPendingQueue();

    expect(fetchImpl).not.toHaveBeenCalled();
    expect(result).toEqual({ synced: 0, retained: 0 });
    expect(document.body.textContent).toContain("Todo sincronizado / No hay cambios pendientes");
  });

  test("Happy path: envia batch al endpoint canonico y limpia la cola", async () => {
    const fetchImpl = jest.fn(async () => ({
      ok: true,
      status: 200,
      json: async () => ({
        results: [{ operation_id: "op-front-sync-001", status: "APPLIED" }],
      }),
    }));
    const { localDb, processPendingQueue, queue } = createSyncHarness({
      queue: [makeOperation()],
      fetchImpl,
    });

    const result = await processPendingQueue();

    expect(fetchImpl).toHaveBeenCalledWith(
      "/api/sync/batch",
      expect.objectContaining({ method: "POST" }),
    );
    expect(fetchImpl.mock.calls[0][0]).not.toBe("/api/sync");
    expect(localDb.clearQueue).toHaveBeenCalledTimes(1);
    expect(queue).toEqual([]);
    expect(result).toEqual({ synced: 1, retained: 0 });
  });

  test("Error: si el servidor devuelve 500, conserva la cola y avisa al usuario", async () => {
    const pending = [makeOperation({ operation_id: "op-front-sync-500" })];
    const fetchImpl = jest.fn(async () => ({
      ok: false,
      status: 500,
      json: async () => ({ detail: "Catastrophic sync failure" }),
    }));
    const { localDb, processPendingQueue, queue } = createSyncHarness({
      queue: pending,
      fetchImpl,
    });

    const result = await processPendingQueue();

    expect(result).toEqual({ synced: 0, retained: 1 });
    expect(localDb.replaceQueue).toHaveBeenCalledWith(pending);
    expect(queue).toEqual(pending);
    expect(document.body.textContent).toContain("No se pudieron sincronizar");
  });

  test("Offline: navigator.onLine=false evita fetch y retiene la cola local", async () => {
    const fetchImpl = jest.fn();
    const { processPendingQueue, queue } = createSyncHarness({
      queue: [makeOperation({ operation_id: "op-front-offline" })],
      fetchImpl,
      online: false,
    });

    const result = await processPendingQueue();

    expect(fetchImpl).not.toHaveBeenCalled();
    expect(result).toEqual({ synced: 0, retained: 1 });
    expect(queue).toHaveLength(1);
    expect(document.body.textContent).toContain("Sin conexion");
  });
});
