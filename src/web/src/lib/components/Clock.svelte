<script lang="ts">
    import {onMount} from "svelte";

    let date = new Date();
    $: hour = date.getHours().toString().padStart(2, "0");
    $: minutes = date.getMinutes().toString().padStart(2, "0");
    $: seconds = date.getSeconds().toString().padStart(2, "0");

    onMount(() => {
        const interval = setInterval(() => {
            date = new Date();
        }, 100);

        return () => clearInterval(interval);
    });
</script>

<span class="w-60">{hour} : {minutes} : {seconds}</span>
