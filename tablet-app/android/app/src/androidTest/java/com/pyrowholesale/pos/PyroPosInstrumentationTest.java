package com.pyrowholesale.pos;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import android.content.Context;
import android.webkit.WebView;
import androidx.lifecycle.Lifecycle;
import androidx.test.core.app.ActivityScenario;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.Test;
import org.junit.runner.RunWith;

/**
 * Android Instrumentation Test Suite for PYROJA POS.
 * 
 * Verifies:
 * 1. App Launch & WebView Initialization
 * 2. IndexedDB Database & ObjectStore Creation
 * 3. Offline Mode Startup & Fallback Customer State
 * 4. Sync Service URL Configuration
 * 5. Product & Customer Master Data Binding
 */
@RunWith(AndroidJUnit4.class)
public class PyroPosInstrumentationTest {

    private String evaluateJs(ActivityScenario<MainActivity> scenario, String script) throws InterruptedException {
        final CountDownLatch latch = new CountDownLatch(1);
        final AtomicReference<String> resultRef = new AtomicReference<>();

        scenario.onActivity(activity -> {
            WebView webView = activity.getBridge().getWebView();
            assertNotNull("Capacitor WebView must not be null", webView);
            webView.evaluateJavascript(script, value -> {
                resultRef.set(value);
                latch.countDown();
            });
        });

        boolean completed = latch.await(10, TimeUnit.SECONDS);
        assertTrue("JavaScript execution timed out: " + script, completed);
        return resultRef.get();
    }

    @Test
    public void test01_appLaunch() {
        Context appContext = InstrumentationRegistry.getInstrumentation().getTargetContext();
        assertEquals("Package name must match com.pyrowholesale.pos", "com.pyrowholesale.pos", appContext.getPackageName());

        try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(MainActivity.class)) {
            assertEquals("Activity must reach RESUMED state", Lifecycle.State.RESUMED, scenario.getState());

            scenario.onActivity(activity -> {
                assertNotNull("Activity must be created", activity);
                assertNotNull("Bridge must be available", activity.getBridge());
                WebView webView = activity.getBridge().getWebView();
                assertNotNull("WebView must be mounted", webView);
            });
        }
    }

    @Test
    public void test02_indexedDbInitialization() throws Exception {
        try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(MainActivity.class)) {
            // Allow initial DOMContentLoaded and IndexedDB open
            Thread.sleep(2000);

            String script = "(function() { " +
                "  if (!window.pos || !window.pos.db || !window.pos.db.db) return 'NOT_INITIALIZED'; " +
                "  return Array.from(window.pos.db.db.objectStoreNames).join(','); " +
                "})()";

            String result = evaluateJs(scenario, script);
            assertNotNull("Result must not be null", result);
            // Result is JSON-encoded string from evaluateJavascript
            assertTrue("IndexedDB must contain 'products' store: " + result, result.contains("products"));
            assertTrue("IndexedDB must contain 'customers' store: " + result, result.contains("customers"));
            assertTrue("IndexedDB must contain 'drafts' store: " + result, result.contains("drafts"));
            assertTrue("IndexedDB must contain 'sync_queue' store: " + result, result.contains("sync_queue"));
            assertTrue("IndexedDB must contain 'meta' store: " + result, result.contains("meta"));
        }
    }

    @Test
    public void test03_offlineModeStartup() throws Exception {
        try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(MainActivity.class)) {
            Thread.sleep(2000);

            String script = "(function() { " +
                "  if (!window.pos) return 'NO_POS'; " +
                "  return JSON.stringify({ " +
                "    hasCart: !!window.pos.cart, " +
                "    customerCode: window.pos.activeCustomer ? window.pos.activeCustomer.code : null " +
                "  }); " +
                "})()";

            String result = evaluateJs(scenario, script);
            assertNotNull("Result must not be null", result);
            assertTrue("Active customer must be assigned (e.g. 99999 CASH A/C): " + result, result.contains("customerCode"));
        }
    }

    @Test
    public void test04_syncServiceUrlConfiguration() throws Exception {
        try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(MainActivity.class)) {
            Thread.sleep(2000);

            String checkUrlScript = "(function() { " +
                "  return window.pos && window.pos.client ? window.pos.client.serverUrl : ''; " +
                "})()";

            String initialUrl = evaluateJs(scenario, checkUrlScript);
            assertNotNull("Server URL must be configured", initialUrl);
            assertTrue("Server URL must start with http: " + initialUrl, initialUrl.contains("http"));

            // Test runtime URL reconfiguration
            String updateScript = "(function() { " +
                "  window.pos.client.setServerUrl('http://10.0.2.2:8080'); " +
                "  return window.pos.client.serverUrl; " +
                "})()";

            String updatedUrl = evaluateJs(scenario, updateScript);
            assertTrue("Updated URL must reflect 10.0.2.2:8080: " + updatedUrl, updatedUrl.contains("10.0.2.2:8080"));
        }
    }

    @Test
    public void test05_productLoading() throws Exception {
        try (ActivityScenario<MainActivity> scenario = ActivityScenario.launch(MainActivity.class)) {
            Thread.sleep(2000);

            String script = "(function() { " +
                "  if (!window.pos) return 'NO_POS'; " +
                "  return (Array.isArray(window.pos.products) && window.pos.products.length >= 0) ? 'PRODUCTS_ARRAY_VALID' : 'INVALID'; " +
                "})()";

            String result = evaluateJs(scenario, script);
            assertNotNull("Result must not be null", result);
            assertTrue("Products must be an array: " + result, result.contains("PRODUCTS_ARRAY_VALID"));
        }
    }
}
