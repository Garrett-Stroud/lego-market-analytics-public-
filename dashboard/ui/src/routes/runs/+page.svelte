<script>
    import { onMount } from 'svelte';

    let runs = [];

    onMount(async () => {
        const res = await fetch("http://localhost:8000/runs");
        runs = await res.json();
    });
</script>

<h2 class="text-3xl font-bold mb-6">Run History</h2>

<ul class="space-y-4">
    {#each runs as run}
        <li class="p-4 bg-white shadow rounded-lg">
            <a href="/runs/{run.id}" class="text-blue-600 hover:underline">
                Run {run.id} — {run.timestamp}
            </a>
        </li>
    {/each}
</ul>
