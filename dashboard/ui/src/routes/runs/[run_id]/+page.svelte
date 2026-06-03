<script>
  export let params;
  let data = null;

  onMount(async () => {
    const res = await fetch(`http://localhost:8000/runs/${params.run_id}`);
    data = await res.json();
  });
</script>

{#if !data}
  <p>Loading run…</p>
{:else}
  <h2 class="text-2xl font-bold mb-4">Run {params.run_id}</h2>

  <pre class="bg-gray-100 p-4 rounded">{JSON.stringify(data, null, 2)}</pre>
{/if}
