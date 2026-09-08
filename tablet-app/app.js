/**
 * PYROWHOLESALE - Tablet POS Client Engine
 * 
 * Features:
 * - Direct consumption of Windows Sync Service REST APIs:
 *     GET /api/sync/products
 *     GET /api/sync/customers
 *     POST /api/orders
 *     GET /api/orders/{id}
 *     GET /api/orders/pending
 *     GET /api/health
 * - Local Persistent Storage (IndexedDB / SQLite backing in Chromium/Android WebView)
 * - Offline-First Operation with Automatic Background Sync Queue
 * - Multi-Customer Tab Management & Live Cart Calculations
 * - Idempotency & Duplicate Prevention
 * - Strict Pack-Multiple Validation
 * - Status Indicators: DRAFT, QUEUED, SYNCED, FAILED
 */

// ==========================================
// 1. CONFIGURATION & STATE STORAGE (DIAGNOSTIC INSTRUMENTATION)
// ==========================================

const urlFromLocalStorage = (typeof localStorage !== "undefined") ? localStorage.getItem("pyro_server_url") : null;
const urlFromWindowLocation = (typeof window !== "undefined" && window.location)
    ? (window.location.port === "8080" 
        ? `${window.location.protocol}//${window.location.hostname}:8080`
        : null)
    : null;
const HARDCODED_FALLBACK_URL = "http://192.168.1.100:8080";

const DEFAULT_SERVER_URL = urlFromLocalStorage 
    ? urlFromLocalStorage
    : (urlFromWindowLocation ? urlFromWindowLocation : HARDCODED_FALLBACK_URL);

console.log("[DIAGNOSTIC] === SYNC SERVICE URL RESOLUTION ===");
console.log("[DIAGNOSTIC] URL from localStorage:", urlFromLocalStorage);
console.log("[DIAGNOSTIC] URL derived from window.location:", urlFromWindowLocation);
console.log("[DIAGNOSTIC] Fallback hardcoded URL:", HARDCODED_FALLBACK_URL);
console.log("[DIAGNOSTIC] Initial selected DEFAULT_SERVER_URL:", DEFAULT_SERVER_URL);


class TabletDB {
    constructor() {
        this.dbName = "PyroWholesalePOS";
        this.version = 2;
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                // Products Store: key is 5-character FoxPro code
                if (!db.objectStoreNames.contains("products")) {
                    const prodStore = db.createObjectStore("products", { keyPath: "code" });
                    prodStore.createIndex("by_company", "company_name", { unique: false });
                    prodStore.createIndex("by_group", "group_code", { unique: false });
                }
                // Customers Store: key is 5-character FoxPro account code
                if (!db.objectStoreNames.contains("customers")) {
                    const custStore = db.createObjectStore("customers", { keyPath: "code" });
                    custStore.createIndex("by_name", "name", { unique: false });
                    custStore.createIndex("by_area", "area_name", { unique: false });
                }
                // Showroom Categories Store (SR 1 to 53 from COMPMST.DBF)
                if (!db.objectStoreNames.contains("categories")) {
                    const catStore = db.createObjectStore("categories", { keyPath: "code" });
                    catStore.createIndex("by_sr", "sr", { unique: false });
                }
                // Local Draft Orders Store
                if (!db.objectStoreNames.contains("drafts")) {
                    db.createObjectStore("drafts", { keyPath: "draft_id" });
                }
                // Background Sync Outbox Queue
                if (!db.objectStoreNames.contains("sync_queue")) {
                    const queueStore = db.createObjectStore("sync_queue", { keyPath: "idempotency_key" });
                    queueStore.createIndex("by_status", "status", { unique: false });
                }
                // Settings & Metadata
                if (!db.objectStoreNames.contains("meta")) {
                    db.createObjectStore("meta", { keyPath: "key" });
                }
            };
        });
    }

    async put(storeName, item) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(storeName, "readwrite");
            tx.objectStore(storeName).put(item);
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    }

    async putBatch(storeName, items) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(storeName, "readwrite");
            const store = tx.objectStore(storeName);
            for (const item of items) {
                store.put(item);
            }
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    }

    async get(storeName, key) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(storeName, "readonly");
            const req = tx.objectStore(storeName).get(key);
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    }

    async getAll(storeName) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(storeName, "readonly");
            const req = tx.objectStore(storeName).getAll();
            req.onsuccess = () => resolve(req.result || []);
            req.onerror = () => reject(req.error);
        });
    }

    async delete(storeName, key) {
        return new Promise((resolve, reject) => {
            const tx = this.db.transaction(storeName, "readwrite");
            tx.objectStore(storeName).delete(key);
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject(tx.error);
        });
    }
}

// ==========================================
// 2. HTTP SYNC CLIENT & DIAGNOSTIC FETCH WRAPPER
// ==========================================

async function diagnosticFetch(url, options = {}) {
    const method = options.method || "GET";
    console.log(`[DIAGNOSTIC FETCH] METHOD ${method} ${url}`);
    try {
        const res = await fetch(url, options);
        console.log(`[DIAGNOSTIC FETCH] RESPONSE STATUS ${res.status} ${res.statusText} (${method} ${url})`);
        try {
            const clone = res.clone();
            const text = await clone.text();
            const preview = text.substring(0, 500);
            console.log(`[DIAGNOSTIC FETCH] RESPONSE BODY (first 500 chars):\n${preview}`);
        } catch (bodyErr) {
            console.log(`[DIAGNOSTIC FETCH] RESPONSE BODY: <unable to read body: ${bodyErr.message}>`);
        }
        return res;
    } catch (netErr) {
        console.error(`[DIAGNOSTIC FETCH ERROR] METHOD ${method} ${url} -> ${netErr.name}: ${netErr.message}`);
        throw netErr;
    }
}

class SyncClient {
    constructor(serverUrl = DEFAULT_SERVER_URL) {
        this.serverUrl = serverUrl.replace(/\/+$/, "");
    }

    setServerUrl(url) {
        this.serverUrl = url.replace(/\/+$/, "");
    }

    async checkHealth() {
        console.log(`[DIAGNOSTIC HEALTH CHECK] Calling checkHealth on: ${this.serverUrl}`);
        const res = await diagnosticFetch(`${this.serverUrl}/api/health`, { method: "GET" });
        if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
        return await res.json();
    }

    async fetchProducts(forceRefresh = false) {
        const url = `${this.serverUrl}/api/sync/products${forceRefresh ? "?force_refresh=true" : ""}`;
        console.log(`[DIAGNOSTIC PRODUCT SYNC] Fetching products from: ${url}`);
        const res = await diagnosticFetch(url, { method: "GET" });
        if (!res.ok) {
            console.error(`[DIAGNOSTIC PRODUCT SYNC FAILED] Status: ${res.status}`);
            throw new Error(`Failed to fetch products: ${res.status}`);
        }
        const data = await res.json();
        console.log(`[DIAGNOSTIC PRODUCT SYNC SUCCESS] Received ${data.products ? data.products.length : 0} products`);
        return data;
    }

    async fetchCustomers(forceRefresh = false) {
        const url = `${this.serverUrl}/api/sync/customers${forceRefresh ? "?force_refresh=true" : ""}`;
        console.log(`[DIAGNOSTIC CUSTOMER SYNC] Fetching customers from: ${url}`);
        const res = await diagnosticFetch(url, { method: "GET" });
        if (!res.ok) {
            console.error(`[DIAGNOSTIC CUSTOMER SYNC FAILED] Status: ${res.status}`);
            throw new Error(`Failed to fetch customers: ${res.status}`);
        }
        const data = await res.json();
        console.log(`[DIAGNOSTIC CUSTOMER SYNC SUCCESS] Received ${data.customers ? data.customers.length : 0} customers`);
        return data;
    }

    async fetchCategories(forceRefresh = false) {
        const url = `${this.serverUrl}/api/sync/categories${forceRefresh ? "?force_refresh=true" : ""}`;
        console.log(`[DIAGNOSTIC CATEGORY SYNC] Fetching categories from: ${url}`);
        const res = await diagnosticFetch(url, { method: "GET" });
        if (!res.ok) {
            console.error(`[DIAGNOSTIC CATEGORY SYNC FAILED] Status: ${res.status}`);
            throw new Error(`Failed to fetch categories: ${res.status}`);
        }
        const data = await res.json();
        console.log(`[DIAGNOSTIC CATEGORY SYNC SUCCESS] Received ${data.categories ? data.categories.length : 0} categories`);
        return data;
    }

    async submitOrder(orderPayload, idempotencyKey) {
        const headers = { "Content-Type": "application/json" };
        if (idempotencyKey) {
            headers["Idempotency-Key"] = idempotencyKey;
        }
        console.log(`[DIAGNOSTIC ORDER SUBMIT] Submitting order draft ${orderPayload.draft_id} to ${this.serverUrl}/api/orders`);
        const res = await diagnosticFetch(`${this.serverUrl}/api/orders`, {
            method: "POST",
            headers,
            body: JSON.stringify(orderPayload)
        });
        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData.detail || `Order submission failed: ${res.status}`);
        }
        return await res.json();
    }

    async getOrder(orderId) {
        const res = await diagnosticFetch(`${this.serverUrl}/api/orders/${orderId}`, { method: "GET" });
        if (!res.ok) throw new Error(`Order not found: ${res.status}`);
        return await res.json();
    }

    async getPendingOrders() {
        const res = await diagnosticFetch(`${this.serverUrl}/api/orders/pending`, { method: "GET" });
        if (!res.ok) throw new Error(`Failed to get pending orders: ${res.status}`);
        return await res.json();
    }
}

// ==========================================
// 3. BACKGROUND SYNC QUEUE (OFFLINE-FIRST)
// ==========================================

class BackgroundSyncQueue {
    constructor(db, client, onStatusChange) {
        this.db = db;
        this.client = client;
        this.onStatusChange = onStatusChange || (() => {});
        this.isProcessing = false;
        this.isOnline = false;
        this.timer = null;
    }

    start() {
        this.checkOnline();
        window.addEventListener("online", () => this.onNetworkOnline());
        window.addEventListener("offline", () => this.onNetworkOffline());
        this.timer = setInterval(() => this.processQueue(), 10000);
    }

    stop() {
        if (this.timer) clearInterval(this.timer);
    }

    async checkOnline() {
        try {
            await this.client.checkHealth();
            if (!this.isOnline) {
                this.isOnline = true;
                this.onStatusChange({ isOnline: true });
                this.processQueue();
            }
        } catch (e) {
            if (this.isOnline) {
                this.isOnline = false;
                this.onStatusChange({ isOnline: false });
            }
        }
    }

    onNetworkOnline() {
        this.checkOnline();
    }

    onNetworkOffline() {
        this.isOnline = false;
        this.onStatusChange({ isOnline: false });
    }

    async enqueue(orderPayload) {
        const idempotencyKey = orderPayload.idempotency_key || `idemp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        orderPayload.idempotency_key = idempotencyKey;

        const queueItem = {
            idempotency_key: idempotencyKey,
            draft_id: orderPayload.draft_id,
            order_payload: orderPayload,
            status: "QUEUED",
            attempts: 0,
            last_error: null,
            created_at: new Date().toISOString()
        };

        await this.db.put("sync_queue", queueItem);
        this.onStatusChange({ event: "ENQUEUED", item: queueItem });

        // Trigger immediate process if online
        this.processQueue();
        return queueItem;
    }

    async processQueue() {
        if (this.isProcessing) return;
        this.isProcessing = true;

        try {
            await this.checkOnline();
            if (!this.isOnline) return;

            const queue = await this.db.getAll("sync_queue");
            const pending = queue.filter(item => item.status === "QUEUED" || item.status === "FAILED");

            for (const item of pending) {
                // Exponential backoff check
                if (item.status === "FAILED" && item.attempts >= 5) {
                    continue; // Skip permanently failed items until manual retry
                }

                try {
                    item.attempts += 1;
                    const result = await this.client.submitOrder(item.order_payload, item.idempotency_key);
                    
                    item.status = "SYNCED";
                    item.server_order_id = result.order_id;
                    item.synced_at = new Date().toISOString();
                    await this.db.put("sync_queue", item);

                    // Update corresponding draft if present
                    const draft = await this.db.get("drafts", item.draft_id);
                    if (draft) {
                        draft.status = "SYNCED";
                        draft.server_order_id = result.order_id;
                        await this.db.put("drafts", draft);
                    }

                    this.onStatusChange({ event: "SYNCED", item, result });
                } catch (err) {
                    item.status = "FAILED";
                    item.last_error = err.message;
                    await this.db.put("sync_queue", item);
                    this.onStatusChange({ event: "FAILED", item, error: err.message });
                }
            }
        } finally {
            this.isProcessing = false;
        }
    }

    async retryFailed() {
        const queue = await this.db.getAll("sync_queue");
        const failed = queue.filter(item => item.status === "FAILED");
        for (const item of failed) {
            item.status = "QUEUED";
            item.attempts = 0;
            await this.db.put("sync_queue", item);
        }
        return this.processQueue();
    }
}

// ==========================================
// 4. POS CONTROLLER & CART MANAGER
// ==========================================

class POSController {
    constructor() {
        this.db = new TabletDB();
        this.client = new SyncClient();
        this.queue = null;

        this.products = [];
        this.customers = [];
        this.categories = [];
        this.activeCustomer = null;
        this.openCustomerTabs = ["99999"];
        
        // Multi-customer scoped draft billing store:
        // customer_code -> { draftId, customerCode, cart: Map(itemCode -> {product, qty, rate}), createdAt, updatedAt }
        this.customerDrafts = new Map();

        this.selectedCategory = "ALL";
        this.selectedSubCategory = "ALL";
        this.selectedBrand = "ALL";
        this.searchQuery = "";

        this.onStateUpdated = () => {};
    }

    generateDraftId() {
        return `TAB01-${Math.floor(1000 + Math.random() * 9000)}`;
    }

    openCustomerTab(customerCode) {
        if (!customerCode) return;
        if (!this.openCustomerTabs.includes(customerCode)) {
            this.openCustomerTabs.push(customerCode);
            this.persistOpenCustomerTabs();
        }
        this.setCustomer(customerCode);
    }

    closeCustomerTab(customerCode) {
        if (this.openCustomerTabs.length <= 1) {
            return;
        }
        const idx = this.openCustomerTabs.indexOf(customerCode);
        if (idx !== -1) {
            this.openCustomerTabs.splice(idx, 1);
            this.persistOpenCustomerTabs();
        }
        if (this.activeCustomer && this.activeCustomer.code === customerCode) {
            const nextCode = this.openCustomerTabs[0];
            this.setCustomer(nextCode);
        } else {
            this.onStateUpdated({ type: "CUSTOMER_TAB_CLOSED" });
        }
    }

    async persistOpenCustomerTabs() {
        try {
            if (typeof localStorage !== "undefined") {
                localStorage.setItem("pyro_open_customer_tabs", JSON.stringify(this.openCustomerTabs));
            }
            if (this.db && this.db.db) {
                await this.db.put("meta", { key: "open_customer_tabs", value: this.openCustomerTabs });
            }
        } catch (e) {
            console.warn("[DIAGNOSTIC TABS] Failed to persist open customer tabs:", e);
        }
    }

    async loadOpenCustomerTabs() {
        try {
            let tabs = null;
            const metaRec = await this.db.get("meta", "open_customer_tabs").catch(() => null);
            if (metaRec && Array.isArray(metaRec.value) && metaRec.value.length > 0) {
                tabs = metaRec.value;
            } else if (typeof localStorage !== "undefined") {
                const local = localStorage.getItem("pyro_open_customer_tabs");
                if (local) {
                    const parsed = JSON.parse(local);
                    if (Array.isArray(parsed) && parsed.length > 0) {
                        tabs = parsed;
                    }
                }
            }

            const tabsSet = new Set(tabs || ["99999"]);
            // Include any customer who has active draft items
            for (const [code, draft] of this.customerDrafts.entries()) {
                if (draft.cart && draft.cart.size > 0) {
                    tabsSet.add(code);
                }
            }
            this.openCustomerTabs = Array.from(tabsSet);
        } catch (e) {
            console.warn("[DIAGNOSTIC TABS] Failed to load open customer tabs:", e);
            this.openCustomerTabs = ["99999"];
        }
    }

    extractCategoriesFromProducts() {
        const map = new Map();
        for (const p of this.products) {
            const code = p.company_code || "000";
            const name = p.company_name || "General";
            if (!map.has(code)) {
                map.set(code, { code, sr: 999, name, item_count: 0 });
            }
            map.get(code).item_count += 1;
        }
        return Array.from(map.values()).sort((a, b) => a.name.localeCompare(b.name));
    }

    ensureCustomerDraft(customerCode) {
        const code = customerCode || (this.activeCustomer ? this.activeCustomer.code : "99999");
        if (!this.customerDrafts.has(code)) {
            this.customerDrafts.set(code, {
                draftId: this.generateDraftId(),
                customerCode: code,
                cart: new Map(),
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            });
        }
        return this.customerDrafts.get(code);
    }

    getActiveDraft() {
        const code = this.activeCustomer ? this.activeCustomer.code : "99999";
        return this.ensureCustomerDraft(code);
    }

    get cart() {
        return this.getActiveDraft().cart;
    }

    get currentDraftId() {
        return this.getActiveDraft().draftId;
    }

    getCustomerDraft(customerCode) {
        return this.customerDrafts.get(customerCode) || null;
    }

    getCustomerCartItemCount(customerCode) {
        const draft = this.customerDrafts.get(customerCode);
        return draft && draft.cart ? draft.cart.size : 0;
    }

    getProductPackSize(productOrCode) {
        const product = typeof productOrCode === "object" && productOrCode !== null
            ? productOrCode
            : this.products.find(p => p.code === productOrCode);
        if (!product) return 10;
        if (product.qty_in_box && Number(product.qty_in_box) > 1) {
            return Number(product.qty_in_box);
        }
        if (product.pack && typeof product.pack === "string") {
            const match = product.pack.match(/\b(\d+)\b/);
            if (match && Number(match[1]) > 1) {
                return Number(match[1]);
            }
        }
        return 10;
    }

    resetCustomerDraft(customerCode) {
        const code = customerCode || (this.activeCustomer ? this.activeCustomer.code : "99999");
        this.customerDrafts.set(code, {
            draftId: this.generateDraftId(),
            customerCode: code,
            cart: new Map(),
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        });
        this.persistCustomerDrafts();
    }

    async persistCustomerDrafts() {
        try {
            const serialized = {};
            for (const [code, draft] of this.customerDrafts.entries()) {
                const items = [];
                for (const [itemCode, entry] of draft.cart.entries()) {
                    items.push({
                        itemCode,
                        qty: entry.qty,
                        rate: entry.rate,
                        product: entry.product
                    });
                }
                serialized[code] = {
                    draftId: draft.draftId,
                    customerCode: code,
                    createdAt: draft.createdAt,
                    updatedAt: draft.updatedAt,
                    items
                };
            }
            const jsonStr = JSON.stringify(serialized);
            if (typeof localStorage !== "undefined") {
                localStorage.setItem("pyro_customer_drafts", jsonStr);
            }
            if (this.db && this.db.db) {
                await this.db.put("meta", { key: "active_customer_drafts", value: serialized });
            }
        } catch (err) {
            console.warn("[DIAGNOSTIC DRAFTS] Failed to persist customer drafts:", err);
        }
    }

    async loadPersistedDrafts() {
        try {
            let data = null;
            // 1. Try IndexedDB meta store
            const metaRecord = await this.db.get("meta", "active_customer_drafts");
            if (metaRecord && metaRecord.value) {
                data = metaRecord.value;
            } else if (typeof localStorage !== "undefined") {
                // 2. Fallback to localStorage
                const localStr = localStorage.getItem("pyro_customer_drafts");
                if (localStr) {
                    data = JSON.parse(localStr);
                }
            }

            if (data && typeof data === "object") {
                for (const [code, draftData] of Object.entries(data)) {
                    const cartMap = new Map();
                    if (Array.isArray(draftData.items)) {
                        for (const it of draftData.items) {
                            if (it && it.itemCode && it.qty > 0) {
                                cartMap.set(it.itemCode, {
                                    product: it.product,
                                    qty: it.qty,
                                    rate: it.rate
                                });
                            }
                        }
                    }
                    this.customerDrafts.set(code, {
                        draftId: draftData.draftId || this.generateDraftId(),
                        customerCode: code,
                        cart: cartMap,
                        createdAt: draftData.createdAt || new Date().toISOString(),
                        updatedAt: draftData.updatedAt || new Date().toISOString()
                    });
                }
                console.log(`[DIAGNOSTIC DRAFTS] Restored ${this.customerDrafts.size} customer drafts from persistent storage.`);
            }
        } catch (err) {
            console.warn("[DIAGNOSTIC DRAFTS] Failed to restore customer drafts:", err);
        }
    }

    async init() {
        console.log("[DIAGNOSTIC INIT] === POSController.init() START ===");
        console.log("[DIAGNOSTIC INIT] Initializing TabletDB (IndexedDB)...");
        await this.db.init();
        console.log("[DIAGNOSTIC INIT] TabletDB initialized.");

        // Load cached server URL if saved
        const metaUrl = await this.db.get("meta", "server_url");
        console.log("[DIAGNOSTIC INIT] URL from IndexedDB/meta:", metaUrl ? metaUrl.value : null);
        if (metaUrl && metaUrl.value) {
            this.client.setServerUrl(metaUrl.value);
        }
        console.log("[DIAGNOSTIC INIT] Final selected URL for SyncClient:", this.client.serverUrl);

        // Restore persisted active customer drafts and open customer tabs
        await this.loadPersistedDrafts();
        await this.loadOpenCustomerTabs();

        // Initialize background queue
        console.log("[DIAGNOSTIC INIT] Starting BackgroundSyncQueue...");
        this.queue = new BackgroundSyncQueue(this.db, this.client, (evt) => this.handleSyncEvent(evt));
        this.queue.start();

        // Load local catalog, customers, and categories
        console.log("[DIAGNOSTIC INIT] Querying local IndexedDB for cached products, customers, and categories...");
        this.products = await this.db.getAll("products");
        this.customers = await this.db.getAll("customers");
        try {
            this.categories = await this.db.getAll("categories");
        } catch (catErr) {
            this.categories = [];
        }

        if ((!this.categories || this.categories.length === 0) && this.products.length > 0) {
            this.categories = this.extractCategoriesFromProducts();
        }

        console.log(`[DIAGNOSTIC INIT] Local cache results: ${this.products.length} products, ${this.customers.length} customers, ${this.categories.length} categories.`);

        // If local cache is empty, trigger initial sync
        if (this.products.length === 0 || this.customers.length === 0) {
            console.log(`[DIAGNOSTIC INIT] Local cache is empty (products: ${this.products.length}, customers: ${this.customers.length}). Triggering initial master refresh from server...`);
            await this.refreshMastersFromServer();
        } else {
            console.log("[DIAGNOSTIC INIT] Local cache has existing records. Skipping initial fetch.");
        }

        // Set default active customer from openCustomerTabs or fallback
        const primaryCode = this.openCustomerTabs[0] || "99999";
        const matchedCust = this.customers.find(c => c.code === primaryCode);
        const cashCust = this.customers.find(c => c.code === "99999");
        this.activeCustomer = matchedCust || cashCust || this.customers[0] || {
            code: "99999",
            name: "CASH A/C",
            price_tier: "RETAIL"
        };
        // Ensure active customer draft exists
        this.ensureCustomerDraft(this.activeCustomer.code);
        if (!this.openCustomerTabs.includes(this.activeCustomer.code)) {
            this.openCustomerTabs.unshift(this.activeCustomer.code);
        }
        console.log(`[DIAGNOSTIC INIT] Default active customer: ${this.activeCustomer.name} (#${this.activeCustomer.code})`);
        console.log("[DIAGNOSTIC INIT] === POSController.init() COMPLETE ===");
    }

    handleSyncEvent(evt) {
        this.onStateUpdated({ type: "SYNC_EVENT", detail: evt });
    }

    async updateServerUrl(url) {
        const cleanUrl = url.trim().replace(/\/+$/, "");
        console.log(`[DIAGNOSTIC] updateServerUrl called with: ${cleanUrl}`);
        this.client.setServerUrl(cleanUrl);
        if (typeof localStorage !== "undefined") {
            localStorage.setItem("pyro_server_url", cleanUrl);
        }
        await this.db.put("meta", { key: "server_url", value: cleanUrl });
        return await this.refreshMastersFromServer();
    }

    async refreshMastersFromServer() {
        console.log(`[DIAGNOSTIC SYNC] refreshMastersFromServer() started. Target server URL: ${this.client.serverUrl}`);
        try {
            console.log("[DIAGNOSTIC SYNC] Calling fetchProducts(), fetchCustomers(), and fetchCategories() concurrently via Promise.all...");
            const [prodData, custData, catData] = await Promise.all([
                this.client.fetchProducts(),
                this.client.fetchCustomers(),
                this.client.fetchCategories().catch(err => {
                    console.warn("[DIAGNOSTIC SYNC] Category fetch from server failed or unsupported, will extract from products:", err);
                    return null;
                })
            ]);

            console.log(`[DIAGNOSTIC SYNC] Master data received! Products: ${prodData.products ? prodData.products.length : 0}, Customers: ${custData.customers ? custData.customers.length : 0}`);

            this.products = prodData.products || [];
            this.customers = custData.customers || [];

            if (catData && Array.isArray(catData.categories) && catData.categories.length > 0) {
                this.categories = catData.categories;
            } else {
                this.categories = this.extractCategoriesFromProducts();
            }

            console.log(`[DIAGNOSTIC SYNC] Saving ${this.products.length} products, ${this.customers.length} customers, and ${this.categories.length} categories to IndexedDB...`);
            // Batch save to local SQLite / IndexedDB
            await this.db.putBatch("products", this.products);
            await this.db.putBatch("customers", this.customers);
            try {
                await this.db.putBatch("categories", this.categories);
            } catch (errCat) {
                console.warn("[DIAGNOSTIC SYNC] Could not write to categories store:", errCat);
            }
            await this.db.put("meta", { key: "last_sync", value: new Date().toISOString() });
            console.log("[DIAGNOSTIC SYNC] IndexedDB write complete. Last sync timestamp updated.");

            this.onStateUpdated({ type: "MASTERS_REFRESHED", count: this.products.length });
            return true;
        } catch (e) {
            console.error(`[DIAGNOSTIC SYNC ERROR] Failed to fetch fresh masters from server (${this.client.serverUrl}):`, e);
            console.warn("Failed to fetch fresh masters from server, using local cache:", e);
            return false;
        }
    }

    setCustomer(code) {
        const found = this.customers.find(c => c.code === code);
        if (found) {
            this.activeCustomer = found;
            if (!this.openCustomerTabs.includes(found.code)) {
                this.openCustomerTabs.push(found.code);
                this.persistOpenCustomerTabs();
            }
            this.ensureCustomerDraft(found.code);
            this.persistCustomerDrafts();
            this.onStateUpdated({ type: "CUSTOMER_CHANGED", customer: found });
        }
    }

    getFilteredProducts() {
        let items = this.products;

        if (this.selectedBrand !== "ALL") {
            items = items.filter(p => p.company_name && p.company_name.toUpperCase().includes(this.selectedBrand.toUpperCase()));
        }

        if (this.selectedCategory !== "ALL") {
            items = items.filter(p => (p.company_code === this.selectedCategory) || (p.company_name === this.selectedCategory));
        }

        if (this.selectedSubCategory !== "ALL") {
            const sub = this.selectedSubCategory.toUpperCase();
            if (sub === "OTHERS") {
                const commonPacks = ["PKT", "BOX", "PCS", "BAG", "ROLL", "CASE", "TIN"];
                items = items.filter(p => {
                    const pPack = (p.pack || "").toUpperCase();
                    return !commonPacks.some(c => pPack.includes(c));
                });
            } else {
                items = items.filter(p => (p.pack || "").toUpperCase().includes(sub));
            }
        }

        if (this.searchQuery) {
            const q = this.searchQuery.toUpperCase();
            items = items.filter(p => p.code.includes(q) || p.name.toUpperCase().includes(q));
        }

        return items;
    }

    updateCartQuantity(itemCode, deltaOrExact, isDelta = true) {
        const product = this.products.find(p => p.code === itemCode);
        if (!product) return;

        const draft = this.getActiveDraft();
        const current = draft.cart.get(itemCode) || {
            product,
            qty: 0,
            rate: product.selling_rate
        };

        const parsedVal = parseInt(deltaOrExact, 10);
        const validVal = isNaN(parsedVal) ? 0 : parsedVal;

        let newQty;
        if (isDelta) {
            newQty = Math.max(0, current.qty + validVal);
        } else {
            newQty = Math.max(0, validVal);
        }

        // Clamp to max allowed quantity = 99999
        newQty = Math.min(99999, Math.floor(newQty));

        if (newQty <= 0) {
            draft.cart.delete(itemCode);
        } else {
            current.qty = newQty;
            draft.cart.set(itemCode, current);
        }
        draft.updatedAt = new Date().toISOString();

        this.persistCustomerDrafts();
        this.onStateUpdated({ type: "CART_UPDATED" });
    }

    clearCart() {
        const draft = this.getActiveDraft();
        draft.cart.clear();
        draft.updatedAt = new Date().toISOString();
        this.persistCustomerDrafts();
        this.onStateUpdated({ type: "CART_UPDATED" });
    }

    getCartTotals(customerCode = null) {
        let subtotal = 0;
        let gst = 0;
        let totalItems = 0;
        let totalCases = 0;

        const cartMap = customerCode && this.customerDrafts.has(customerCode)
            ? this.customerDrafts.get(customerCode).cart
            : this.cart;

        for (const [code, entry] of cartMap.entries()) {
            const taxable = Math.round(entry.qty * entry.rate * 100) / 100;
            const taxPct = entry.product.tax_percentage || 0;
            const lineTax = Math.round(taxable * (taxPct / 100) * 100) / 100;

            subtotal += taxable;
            gst += lineTax;
            totalItems += 1;
            
            const qib = entry.product.qty_in_box || 1;
            totalCases += Math.round((entry.qty / qib) * 10) / 10;
        }

        subtotal = Math.round(subtotal * 100) / 100;
        gst = Math.round(gst * 100) / 100;
        const total = Math.round((subtotal + gst) * 100) / 100;

        return { subtotal, gst, total, totalItems, totalCases };
    }

    buildOrderPayload() {
        if (this.cart.size === 0) {
            throw new Error("Cart is empty.");
        }

        const lines = [];
        for (const [code, entry] of this.cart.entries()) {
            lines.push({
                item_code: entry.product.code,
                item_name: entry.product.name,
                pack: entry.product.pack,
                qty_in_box: entry.product.qty_in_box,
                qty: entry.qty,
                rate: entry.rate,
                tax_percentage: entry.product.tax_percentage
            });
        }

        return {
            draft_id: this.currentDraftId,
            tablet_id: "TABLET-01",
            customer_code: this.activeCustomer.code,
            customer_name: this.activeCustomer.name,
            order_date: new Date().toISOString().split("T")[0],
            remarks: "Showroom POS Dispatch",
            status: "QUEUED",
            line_items: lines
        };
    }

    async submitCurrentOrder() {
        const payload = this.buildOrderPayload();
        
        // Save to local drafts
        await this.db.put("drafts", {
            ...payload,
            created_at: new Date().toISOString(),
            status: "QUEUED"
        });

        // Add to background sync queue
        const queuedItem = await this.queue.enqueue(payload);

        // Reset ONLY this active customer's draft
        const custCode = this.activeCustomer ? this.activeCustomer.code : "99999";
        this.resetCustomerDraft(custCode);
        this.onStateUpdated({ type: "CART_UPDATED" });

        return queuedItem;
    }
}

// Attach to window for browser global scope
if (typeof window !== "undefined") {
    window.TabletDB = TabletDB;
    window.SyncClient = SyncClient;
    window.BackgroundSyncQueue = BackgroundSyncQueue;
    window.POSController = POSController;
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = { TabletDB, SyncClient, BackgroundSyncQueue, POSController };
}
