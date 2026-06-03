<script>
  export let params;
  let data = null;
  let loading = true;

  onMount(async () => {
    const res = await fetch(`http://localhost:8000/set/${params.set_number}`);
    data = await res.json();
    loading = false;
  });
</script>

{#if loading}
  <p>Loading set details…</p>
{:else}
  <h2 class="text-2xl font-bold mb-4">{data.name}</h2>

  <div class="grid grid-cols-2 gap-6">
    <div class="p-4 bg-white shadow rounded">
      <h3 class="font-semibold mb-2">Metadata</h3>
      <p>Set Number: {data.set_number}</p>
      <p>Theme: {data.theme}</p>
      <p>Pieces: {data.pieces}</p>
    </div>

    <div class="p-4 bg-white shadow rounded">
      <h3 class="font-semibold mb-2">Current Price</h3>
      <p class="text-xl font-bold">${data.current_price}</p>
    </div>
  </div>
{/if}
