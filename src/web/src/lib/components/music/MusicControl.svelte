<script lang="ts">
    import {popup, type PopupSettings, ProgressBar, ProgressRadial} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faBackwardStep, faForwardStep, faPause, faPlay, faRepeat, faShuffle, faStop, faVolumeHigh, faVolumeLow, faVolumeMute} from "@fortawesome/free-solid-svg-icons";

    import weckpiCore from "$lib/BackendConnection/WeckPiCoreConnection";
    import {musicPlaying, musicPosition, musicQueue, musicQueuePosition, musicRepeat, musicShuffle, musicVolume} from "$lib/BackendConnection/ParameterStore";
    import {minutesToTime} from "$lib/utilities/DateTime";

    //region Volume Slider
    function volumeIcon(volume: number) {
        if (volume === 0) return faVolumeMute;
        if (volume < 50) return faVolumeLow;
        return faVolumeHigh;
    }

    let volumeButtonClickedMultipleTimes = false;
    let oldVolume = 0;

    const volumePopupSettings: PopupSettings = {
        event: "click",
        target: "volumePopup",
        placement: "top",
        state: (e: Record<string, boolean>) => {
            if (!e.state) volumeButtonClickedMultipleTimes = false;
        }
    };

    function onVolumeButtonClick() {
        if (volumeButtonClickedMultipleTimes) {
            [oldVolume, $musicVolume] = [$musicVolume, oldVolume];
        }
        volumeButtonClickedMultipleTimes = true;
    }

    //endregion
</script>

<div class="bg-surface-100-800-token p-4 grid gap-6" style="grid-template-columns: 20% 1fr 20%">
    <div class="flex flex-row gap-4 overflow-hidden whitespace-nowrap">
        {#if $musicQueue && $musicQueue.length >= 1}
            <img alt="Album Cover" class="h-[90px] rounded-lg" src={$musicQueue[$musicQueuePosition].image}>
            <div>
                <span class="font-bold">{$musicQueue[$musicQueuePosition].title}</span><br/>
                <span>{$musicQueue[$musicQueuePosition].artist}</span><br/>
                <span>{$musicQueue[$musicQueuePosition].album}</span>
            </div>
        {:else}
            <ProgressRadial class="h-10 w-10" stroke={120}/>
        {/if}
    </div>

    <div class="flex flex-col gap-4">
        <div class="flex place-content-center gap-4">
            <button class="btn-icon" class:variant-ghost={!$musicShuffle} class:variant-ghost-primary={$musicShuffle}
                    on:click={() => $musicShuffle = !$musicShuffle}>
                <Fa icon={faShuffle}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.previousSong")}>
                <Fa icon={faBackwardStep}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={() => $musicPlaying = !$musicPlaying}>
                <Fa icon={$musicPlaying ? faPause : faPlay}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.nextSong")}>
                <Fa icon={faForwardStep}/>
            </button>

            <button class="btn-icon" class:variant-ghost={!$musicRepeat} class:variant-ghost-primary={$musicRepeat}
                    on:click={() => $musicRepeat = !$musicRepeat}>
                <Fa icon={faRepeat}/>
            </button>
        </div>

        <div class="flex place-items-center gap-6">
            <span>{minutesToTime($musicPosition)}</span>
            <ProgressBar max={1} value={$musicPosition / $musicQueue[$musicQueuePosition].duration}/>
            <span>{minutesToTime($musicQueue[$musicQueuePosition].duration)}</span>
        </div>
    </div>

    <div class="flex place-items-center place-content-end gap-4 mr-10">
        <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.stop")}>
            <Fa icon={faStop}/>
        </button>

        <button class="btn-icon variant-ghost" on:click={onVolumeButtonClick} use:popup={volumePopupSettings}>
            <Fa icon={volumeIcon($musicVolume)}/>
        </button>
    </div>

    <div class="p-4 bg-surface-400-500-token rounded-lg" data-popup="volumePopup">
        <input bind:value={$musicVolume} class="h-20" id="volumeSlider" max="100" orient="vertical" type="range"/>
        <div class="arrow variant-filled-surface"></div>
    </div>
</div>

<style lang="postcss">
    #volumeSlider {
        @apply bg-transparent;
    }

    #volumeSlider::-moz-range-track,
    #volumeSlider::-webkit-slider-runnable-track {
        @apply h-full w-2 rounded-token bg-surface-50 cursor-pointer;
    }

    #volumeSlider::-moz-range-thumb,
    #volumeSlider::-webkit-slider-thumb {
        @apply h-4 w-4 rounded-full bg-surface-50 cursor-pointer border-none;
    }
</style>
