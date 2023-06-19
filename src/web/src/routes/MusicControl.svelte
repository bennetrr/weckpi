<script lang="ts">
    import {musicMetadata, musicPosition} from "$lib/stores/ContentStore"
    import {minutesToTime} from "$lib/helpers/DateTimeHelpers";

    import {ProgressBar} from "@skeletonlabs/skeleton";

    //@ts-ignore
    import Fa from "svelte-fa";
    import { faBackwardStep, faForwardStep, faPlay, faRepeat, faShuffle, faVolumeHigh } from "@fortawesome/free-solid-svg-icons";
</script>

<div class="bg-surface-100-800-token p-4 grid gap-6" style="grid-template-columns: 20% 1fr 20%">
    <div class="flex flex-row gap-4 overflow-hidden whitespace-nowrap">
        <img src={$musicMetadata.image_uri} alt="Image" class="h-[90px] rounded-lg">
        <div>
            <span class="font-bold" title={$musicMetadata.title}>{$musicMetadata.title}</span><br/>
            <span title={$musicMetadata.artist}>{$musicMetadata.artist}</span><br/>
            <span title={$musicMetadata.album}>{$musicMetadata.album}</span>
        </div>
    </div>

    <div class="flex flex-col gap-4">
        <div class="flex place-content-center gap-4">
            <button class="btn-icon variant-ghost"><Fa icon={faShuffle}/></button>
            <button class="btn-icon variant-ghost"><Fa icon={faBackwardStep}/></button>
            <button class="btn-icon variant-ghost"><Fa icon={faPlay}/></button>
            <button class="btn-icon variant-ghost"><Fa icon={faForwardStep}/></button>
            <button class="btn-icon variant-ghost"><Fa icon={faRepeat}/></button>
        </div>

        <div class="flex place-items-center gap-6">
            <span>{minutesToTime($musicPosition)}</span>
            <ProgressBar value={$musicPosition / $musicMetadata.duration} max={1}/>
            <span>{minutesToTime($musicMetadata.duration)}</span>
        </div>
    </div>

    <div class="flex place-items-center place-content-end gap-4">
        <button class="btn-icon variant-ghost"><Fa icon={faVolumeHigh}/></button>
    </div>
</div>
