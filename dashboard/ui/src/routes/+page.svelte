<script>
    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    let opportunities = $state([]);
    let loading = $state(true);
    let error = $state(null);
    let selected = $state(null);

    // SEARCH
    let query = $state("");

    // SORTING
    let sortKey = $state("score");
    let sortDir = $state("desc");

    // HISTORY FOR SELECTED SET (run-to-run)
    let history = $state([]);

    // CHART INSTANCE
    let chartInstance = null;

    function sortBy(key) {
        if (sortKey === key) {
            sortDir = sortDir === "asc" ? "desc" : "asc";
        } else {
            sortKey = key;
            sortDir = "desc";
        }
    }

    function formatMoney(v) {
        return `$${v.toFixed(2)}`;
    }

    function roiColor(roi) {
    if (roi >= 0.50) return "text-green-600 font-semibold";   // 50%+
    if (roi >= 0.20) return "text-yellow-600 font-semibold";  // 20–50%
    return "text-red-600 font-semibold";                      // <20%
}


    onMount(async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/opportunities/latest");
            if (!res.ok) throw new Error("Failed to load opportunities");
            opportunities = await res.json();
        } catch (e) {
            error = e.message;
        } finally {
            loading = false;
        }
    });

    // FILTERED LIST (Svelte 5 runes)
    let filtered = $derived(
        opportunities.filter(o =>
            o.product_key.toLowerCase().includes(query.toLowerCase())
        )
    );

    // SORTED LIST (Svelte 5 runes)
    let sorted = $derived(
        [...filtered].sort((a, b) => {
            const x = a[sortKey];
            const y = b[sortKey];
            return sortDir === "asc" ? x - y : y - x;
        })
    );

    // FETCH RUN-TO-RUN HISTORY WHEN A SET IS SELECTED
    $effect(async () => {
        if (!selected) {
            history = [];
            return;
        }

        try {
            const res = await fetch(
                `http://127.0.0.1:8000/opportunities/set/${selected.product_key}`
            );
            if (!res.ok) throw new Error("Failed to load history");
            // ordered by created_at DESC in repo; reverse so oldest -> newest
            const rows = await res.json();
            history = rows.slice().reverse();
        } catch (e) {
            console.error(e);
            history = [];
        }
    });

    // BUILD MULTI-LINE CHART (PRICE + PROFIT + SCORE + ROI) FROM HISTORY
    $effect(() => {
        if (!selected || history.length === 0) {
            if (chartInstance) {
                chartInstance.destroy();
                chartInstance = null;
            }
            return;
        }

        const canvas = document.getElementById("priceHistoryChart");
        if (!canvas) return;

        if (chartInstance) {
            chartInstance.destroy();
            chartInstance = null;
        }

        const labels = history.map((_, idx) => `Run ${idx + 1}`);

        const sellPrices = history.map(h => h.sell_price);
        const profits = history.map(h => h.profit);
        const scores = history.map(h => h.score);
        const rois = history.map(h => h.roi);

        const dark = document.documentElement.classList.contains("dark");
        const axisColor = dark ? "#e5e7eb" : "#374151";

        chartInstance = new Chart(canvas, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: "Sell Price",
                        data: sellPrices,
                        borderColor: "#6366f1",
                        backgroundColor: "rgba(99, 102, 241, 0.15)",
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: "Profit",
                        data: profits,
                        borderColor: "#22c55e",
                        backgroundColor: "rgba(34, 197, 94, 0.15)",
                        tension: 0.3,
                        pointRadius: 3
                    },
                    {
                        label: "Score",
                        data: scores,
                        borderColor: "#f97316",
                        backgroundColor: "rgba(249, 115, 22, 0.15)",
                        tension: 0.3,
                        pointRadius: 3,
                        yAxisID: "y1"
                    },
                    {
                        label: "ROI",
                        data: rois,
                        borderColor: "#e11d48",
                        backgroundColor: "rgba(225, 29, 72, 0.15)",
                        tension: 0.3,
                        pointRadius: 3,
                        yAxisID: "y1"
                    }
                ]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: "index",
                    intersect: false
                },
                plugins: {
                    legend: {
                        labels: {
                            color: axisColor
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: axisColor },
                        grid: { color: dark ? "#4b5563" : "#e5e7eb" }
                    },
                    y: {
                        position: "left",
                        ticks: { color: axisColor },
                        grid: { color: dark ? "#4b5563" : "#e5e7eb" }
                    },
                    y1: {
                        position: "right",
                        ticks: { color: axisColor },
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });
    });
</script>

<!-- SEARCH BAR -->
<div class="mb-6 animate-fade-in">
    <input
        type="text"
        placeholder="Search by set number…"
        bind:value={query}
        class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
    />
</div>

<!-- SORTING BUTTONS -->
<div class="flex gap-4 mb-6 animate-fade-in">
    <button onclick={() => sortBy("score")} class="px-3 py-2 rounded bg-gray-200 dark:bg-gray-700">
        Score
    </button>
    <button onclick={() => sortBy("roi")} class="px-3 py-2 rounded bg-gray-200 dark:bg-gray-700">
        ROI
    </button>
    <button onclick={() => sortBy("profit")} class="px-3 py-2 rounded bg-gray-200 dark:bg-gray-700">
        Profit
    </button>
</div>

{#if loading}
    <div class="text-center text-gray-600 text-lg">Loading opportunities…</div>

{:else if error}
    <div class="text-center text-red-600 text-lg">{error}</div>

{:else}

    <!-- CARD GRID -->
    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8 animate-fade-in">
        {#each sorted as opp}
    <div
        class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm p-6 space-y-4
               hover:-translate-y-1 hover:shadow-xl transition-all duration-200">

        <!-- IMAGE -->
        {#if opp.image_url}
            <img
                src={opp.image_url}
                alt={opp.title}
                class="w-full h-40 object-contain rounded-md mb-3 bg-gray-50 dark:bg-gray-900 p-2"
                loading="lazy"
            />
        {/if}

        <!-- TITLE + SET NUMBER + SCORE BADGE -->
        <div class="flex justify-between items-start">
            <div>
                <h3 class="text-lg font-semibold leading-tight">{opp.title}</h3>
                <div class="text-xs text-gray-500 dark:text-gray-400">{opp.product_key}</div>
            </div>

            <span class="px-2 py-1 text-sm rounded-md bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300">
                Score {opp.score.toFixed(2)}
            </span>
        </div>

        <!-- PRICE + PROFIT + ROI -->
        <div class="text-sm space-y-1 pt-2">

            <div class="flex justify-between">
                <strong>Buy:</strong>
                <span>{formatMoney(opp.buy_price)}</span>
            </div>

            <div class="flex justify-between">
                <strong>Sell:</strong>
                <span>{formatMoney(opp.sell_price)}</span>
            </div>

            <div class="flex justify-between {roiColor(opp.profit)}">
                <strong>Profit:</strong>
                <span>{formatMoney(opp.profit)}</span>
            </div>

            <div class="flex justify-between {roiColor(opp.roi)}">
                <strong>ROI:</strong>
                <span>{(opp.roi * 100).toFixed(1)}%</span>
            </div>

            <div class="flex justify-between text-gray-600 dark:text-gray-300">
                <strong>Margin:</strong>
                <span>{(opp.profit / opp.sell_price * 100).toFixed(1)}%</span>
            </div>
        </div>

        <!-- ACTION BUTTONS -->
        <div class="flex gap-3 pt-4">
            <button
                class="flex-1 px-3 py-2 rounded-md bg-gray-900 text-white hover:bg-gray-700 transition"
                onclick={() => selected = opp}
            >
                Details
            </button>

            <a
                href={opp.buy_url}
                target="_blank"
                class="flex-1 px-3 py-2 rounded-md bg-gradient-to-r from-blue-500 to-purple-600 text-white text-center hover:opacity-90 transition"
            >
                Buy
            </a>
        </div>
    </div>
{/each}

    </div>

{/if}

<!-- MODAL WITH MULTI-LINE RUN-TO-RUN CHART -->
{#if selected}
<div class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 w-full max-w-2xl p-6 space-y-6">

        <h3 class="text-xl font-bold">
    {selected.title} — Run-to-run metrics
</h3>


        {#if history.length === 0}
            <div class="text-sm text-gray-500 dark:text-gray-400">
                No historical runs found for this set yet.
            </div>
        {:else}
            <div class="w-full h-64">
                <canvas id="priceHistoryChart"></canvas>
            </div>
        {/if}

        <h3 class="text-xl font-bold">Score Details</h3>

        <pre class="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg text-sm overflow-auto max-h-80">
{JSON.stringify(selected.score_details, null, 2)}
        </pre>

        <button
            class="w-full px-4 py-2 rounded-md bg-gray-900 text-white hover:bg-gray-700 transition"
            onclick={() => selected = null}
        >
            Close
        </button>
    </div>
</div>
{/if}
