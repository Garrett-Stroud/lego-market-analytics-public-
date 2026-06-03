<script>
    import "../app.css";

    let dark = $state(false);
    let running = $state(false);

    function toggleDark() {
        dark = !dark;
        document.documentElement.classList.toggle("dark", dark);
    }

    async function runNow() {
        running = true;
        try {
            const res = await fetch("http://127.0.0.1:8000/pipeline/run", {
                method: "POST"
            });

            if (!res.ok) throw new Error("Pipeline failed to start");

            alert("Pipeline started! Refresh in ~30–60 seconds.");
        } catch (e) {
            alert("Error starting pipeline: " + e.message);
        } finally {
            running = false;
        }
    }
</script>

<div class="min-h-screen flex bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">

    <!-- Sidebar -->
    <aside class="hidden md:flex flex-col w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 shadow-sm">
        <div class="p-6 border-b border-gray-100 dark:border-gray-700">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                LEGO Arbitrage
            </h1>
        </div>

        <nav class="flex-1 p-4 space-y-1">
            <a href="/" class="block px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 font-medium">
                Opportunities
            </a>
            <a href="/runs" class="block px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 font-medium">
                Runs
            </a>
            <a href="/snapshots" class="block px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 font-medium">
                Snapshots
            </a>
        </nav>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">

        <!-- Top Header -->
        <header class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm p-4 flex items-center justify-between">

            <h2 class="text-xl font-semibold dark:text-white">Dashboard</h2>

            <div class="flex items-center gap-3">

                <!-- Run Now Button -->
                <button
                    onclick={runNow}
                    class="px-3 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-500 disabled:opacity-50"
                    disabled={running}
                >
                    {running ? "Running…" : "Run Now"}
                </button>

                <!-- Dark Mode Toggle -->
                <button
                    onclick={toggleDark}
                    class="px-3 py-2 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                >
                    {dark ? "Light Mode" : "Dark Mode"}
                </button>

            </div>
        </header>

        <!-- Routed Pages -->
        <main class="flex-1 p-8">
            <slot />
        </main>
    </div>
</div>
