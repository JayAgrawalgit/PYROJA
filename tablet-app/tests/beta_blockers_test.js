const assert = require("assert");

// Mock browser globals for Node test environment
global.window = {};
global.localStorage = {
    _data: {},
    getItem(k) { return this._data[k] || null; },
    setItem(k, v) { this._data[k] = String(v); },
    removeItem(k) { delete this._data[k]; },
    clear() { this._data = {}; }
};

const { POSController } = require("../app.js");

async function runTests() {
    console.log("=== RUNNING BETA BLOCKERS INTEGRATION SUITE ===");

    const pos = new POSController();

    // Mock DB layer for in-memory testing
    const memoryStores = {
        products: new Map(),
        customers: new Map(),
        categories: new Map(),
        subcategories: new Map(),
        drafts: new Map(),
        sync_queue: new Map(),
        meta: new Map()
    };

    pos.db = {
        async init() { return true; },
        async get(store, key) {
            return memoryStores[store].get(key) || null;
        },
        async getAll(store) {
            return Array.from(memoryStores[store].values());
        },
        async put(store, val) {
            const key = val.code || val.key || val.draft_id || val.idempotency_key;
            memoryStores[store].set(key, val);
            return key;
        },
        async putBatch(store, items) {
            for (const item of items) {
                const key = item.code || item.key || item.draft_id || item.idempotency_key;
                memoryStores[store].set(key, item);
            }
            return items.length;
        },
        async delete(store, key) {
            return memoryStores[store].delete(key);
        }
    };

    // 1. Test Mock Master Data
    pos.products = [
        { code: "00001", name: "10 CM SPARKLES RED", company_code: "001", company_name: "STANDARD SPARKLERS", pack: "PKT", qty_in_box: 10, selling_rate: 45.0, tax_percentage: 18.0, stock_on_hand: 50 },
        { code: "00002", name: "15 CM SPARKLES GREEN", company_code: "001", company_name: "STANDARD SPARKLERS", pack: "BOX", qty_in_box: 5, selling_rate: 65.0, tax_percentage: 18.0, stock_on_hand: 30 },
        { code: "00003", name: "GROUND CHAKKAR DELUXE", company_code: "002", company_name: "CHAKKAR DELUXE", pack: "BOX", qty_in_box: 10, selling_rate: 120.0, tax_percentage: 18.0, stock_on_hand: 40 },
        { code: "00004", name: "FLOWER POT SPECIAL", company_code: "002", company_name: "CHAKKAR DELUXE", pack: "PCS", qty_in_box: 1, selling_rate: 80.0, tax_percentage: 18.0, stock_on_hand: 25 },
        { code: "00005", name: "FANCY COLOR FOUNTAIN", company_code: "003", company_name: "FOUNTAIN WORLD", pack: "TIN", qty_in_box: 4, selling_rate: 250.0, tax_percentage: 18.0, stock_on_hand: 15 },
        { code: "00006", name: "MATCHES & FUSES", company_code: "004", company_name: "SUNDRIES", pack: "MISC_JAR", qty_in_box: 1, selling_rate: 20.0, tax_percentage: 18.0, stock_on_hand: 100 }
    ];

    pos.customers = [
        { code: "99999", name: "CASH A/C", price_tier: "RETAIL", area_name: "LOCAL" },
        { code: "00010", name: "SHREE GANESH TRADERS", price_tier: "WHOLESALE", area_name: "SIVAKASI" },
        { code: "00020", name: "BALAJI FIREWORKS", price_tier: "DEALER", area_name: "MADURAI" }
    ];

    pos.categories = [
        { code: "001", sr: 1, name: "STANDARD SPARKLERS", item_count: 2 },
        { code: "002", sr: 2, name: "CHAKKAR DELUXE", item_count: 2 },
        { code: "003", sr: 3, name: "FOUNTAIN WORLD", item_count: 1 },
        { code: "004", sr: 4, name: "SUNDRIES", item_count: 1 }
    ];

    pos.subcategories = [
        { code: "PKT", name: "PKT", item_count: 1 },
        { code: "BOX", name: "BOX", item_count: 2 },
        { code: "PCS", name: "PCS", item_count: 1 },
        { code: "BAG", name: "BAG", item_count: 0 },
        { code: "ROLL", name: "ROLL", item_count: 0 },
        { code: "TIN", name: "TIN", item_count: 1 },
        { code: "BUNDLE", name: "BUNDLE", item_count: 0 },
        { code: "OTHERS", name: "OTHERS", item_count: 1 }
    ];

    // TEST 1: Categories & Product Filtering
    console.log("Test 1: Category filtering...");
    pos.selectedCategory = "001";
    let filtered = pos.getFilteredProducts();
    assert.strictEqual(filtered.length, 2, "Should filter exactly 2 products for category 001");
    assert(filtered.every(p => p.company_code === "001"));

    // TEST 2: Subcategory Pack Filtering
    console.log("Test 2: Subcategory Pack filtering combined with category...");
    pos.selectedSubCategory = "PKT";
    filtered = pos.getFilteredProducts();
    assert.strictEqual(filtered.length, 1, "Category 001 with PKT pack should yield 1 product");
    assert.strictEqual(filtered[0].code, "00001");

    pos.selectedCategory = "ALL";
    pos.selectedSubCategory = "BOX";
    filtered = pos.getFilteredProducts();
    assert.strictEqual(filtered.length, 2, "ALL with BOX pack should yield 2 products");

    pos.selectedSubCategory = "OTHERS";
    filtered = pos.getFilteredProducts();
    assert.strictEqual(filtered.length, 1, "ALL with OTHERS pack should yield 1 misc item");
    assert.strictEqual(filtered[0].code, "00006");

    pos.selectedCategory = "ALL";
    pos.selectedSubCategory = "ALL";

    // TEST 3: Multi-Tab Cart Isolation
    console.log("Test 3: Multi-Tab Cart Isolation...");
    // Open Cash A/C
    pos.setCustomer("99999");
    assert.strictEqual(pos.activeCustomer.code, "99999");
    pos.updateCartQuantity("00001", 10, true);
    pos.updateCartQuantity("00002", 5, true);

    const cashTotals = pos.getCartTotals("99999");
    assert.strictEqual(cashTotals.totalItems, 2);
    assert.strictEqual(pos.cart.size, 2);

    // Open second customer tab
    console.log("Opening customer tab 00010...");
    pos.openCustomerTab("00010");
    assert.strictEqual(pos.activeCustomer.code, "00010");
    assert.strictEqual(pos.cart.size, 0, "New customer cart must be strictly isolated and empty");

    // Add item to customer 00010
    pos.updateCartQuantity("00003", 20, true);
    assert.strictEqual(pos.cart.size, 1);
    const cust10Totals = pos.getCartTotals("00010");
    assert.strictEqual(cust10Totals.totalItems, 1);

    // Switch back to Cash A/C
    console.log("Switching back to Cash A/C...");
    pos.setCustomer("99999");
    assert.strictEqual(pos.activeCustomer.code, "99999");
    assert.strictEqual(pos.cart.size, 2, "Cash A/C cart must retain its 2 items");
    assert.strictEqual(pos.cart.get("00001").qty, 10);
    assert.strictEqual(pos.cart.get("00002").qty, 5);

    // Verify Cash and Customer drafts never mix
    assert.strictEqual(pos.getCustomerCartItemCount("99999"), 2);
    assert.strictEqual(pos.getCustomerCartItemCount("00010"), 1);

    // TEST 4: Create New Order with unknown customer
    console.log("Test 4: Create New Order resilient customer handling...");
    pos.openCustomerTab("88888");
    assert.strictEqual(pos.activeCustomer.code, "88888");
    assert.strictEqual(pos.activeCustomer.name, "CUSTOMER #88888");
    assert(pos.openCustomerTabs.includes("88888"));

    // TEST 5: Mock refreshMastersFromServer
    console.log("Test 5: refreshMastersFromServer structured response...");
    pos.client = {
        serverUrl: "http://127.0.0.1:8080",
        async fetchProducts() { return { products: pos.products }; },
        async fetchCustomers() { return { customers: pos.customers }; },
        async fetchCategories() { return { categories: pos.categories }; },
        async fetchSubcategories() { return { subcategories: pos.subcategories }; }
    };

    const syncRes = await pos.refreshMastersFromServer();
    assert.strictEqual(syncRes.success, true);
    assert.strictEqual(syncRes.productsCount, 6);
    assert.strictEqual(syncRes.customersCount, 3);
    assert.strictEqual(syncRes.categoriesCount, 4);
    assert.strictEqual(syncRes.subcategoriesCount, 8);
    assert(typeof syncRes.lastSync === "string");
    assert.strictEqual(pos.lastSync, syncRes.lastSync);

    console.log("=== ALL BETA BLOCKERS TESTS PASSED! ===");
}

runTests().catch(err => {
    console.error("TEST FAILED:", err);
    process.exit(1);
});
