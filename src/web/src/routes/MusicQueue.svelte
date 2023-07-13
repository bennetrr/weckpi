<script lang="ts">
    import {debug} from "debug";

    import {ProgressRadial} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faPlay, faTrash} from "@fortawesome/free-solid-svg-icons";

    import weckpiCore from "$lib/BackendConnection/WeckPiCoreConnection";
    import {musicQueue, musicQueuePosition} from "$lib/BackendConnection/ParameterStore";
    import {minutesToTime} from "$lib/helpers/DateTimeHelpers";

    const log = debug("weckpiWeb:musicQueue");
</script>

<div class="bg-surface-100-800-token p-4 h-full w-[450px]">
    {#each $musicQueue as queueElement, i}
    <div class="flex flex-row gap-4 overflow-hidden whitespace-nowrap my-3 p-3 bg-surface-200-700-token rounded-lg hover:brightness-[115%] cursor-pointer border-primary-50-900-token" class:border-2={i===$musicQueuePosition} on:click={() => $musicQueuePosition = i}>
        {#if i === $musicQueuePosition}
            <Fa class="my-auto" icon={faPlay}/>
            {:else}
        <span class="my-auto">{i}</span>
        {/if}
        <img alt="Album Cover" class="h-[90px] rounded-lg" src={queueElement.image}>
        <div>
            <span class="font-bold">{queueElement.title}</span><br/>
            <span>{queueElement.artist}</span><br/>
            <span>{queueElement.album}</span><br/>
            <span>{minutesToTime(queueElement.duration)}</span>
        </div>
    </div>
    {/each}
</div>
