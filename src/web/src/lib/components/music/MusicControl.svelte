<script lang="ts">
    import {popup, type PopupSettings, ProgressBar, ProgressRadial} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faBackwardStep, faForwardStep, faPause, faPlay, faRepeat, faShuffle, faStop, faVolumeHigh, faVolumeLow, faVolumeMute} from "@fortawesome/free-solid-svg-icons";

    import appState from "$lib/app-state/app-state";
    import {minutesToTime} from "$lib/utilities/DateTime";
    import weckpiCore from "$lib/app-state/backend-connection";

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
            const temp = oldVolume;
            oldVolume = appState.music.volume;
            appState.music.setVolume(temp);
        }
        volumeButtonClickedMultipleTimes = true;
    }

    function onVolumeSliderChange(event: Event) {
        appState.music.setVolume((event.target as HTMLInputElement).valueAsNumber);
    }

    //endregion
</script>

<div class="bg-surface-100-800-token p-4 grid gap-6" style="grid-template-columns: 20% 1fr 20%">
    <div class="flex flex-row gap-4 overflow-hidden whitespace-nowrap">
        {#if $appState.music.queue && $appState.music.queue.length >= 1}
            <img alt="Album Cover" class="h-[90px] rounded-lg" src={appState.music.currentItem().image}>
            <div>
                <span class="font-bold">{appState.music.currentItem().title}</span><br/>
                <span>{appState.music.currentItem().artist}</span><br/>
                <span>{appState.music.currentItem().album}</span>
            </div>
        {:else}
            <ProgressRadial class="h-10 w-10" stroke={120}/>
        {/if}
    </div>

    <div class="flex flex-col gap-4">
        <div class="flex place-content-center gap-4">
            <button class="btn-icon" class:variant-ghost={!$appState.music.shuffle}
                    class:variant-ghost-primary={$appState.music.shuffle}
                    on:click={appState.music.toggleShuffle}>
                <Fa icon={faShuffle}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.previousSong")}>
                <Fa icon={faBackwardStep}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={appState.music.toggleIsPlaying}>
                <Fa icon={$appState.music.isPlaying ? faPause : faPlay}/>
            </button>

            <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.nextSong")}>
                <Fa icon={faForwardStep}/>
            </button>

            <button class="btn-icon" class:variant-ghost={!$appState.music.repeat}
                    class:variant-ghost-primary={$appState.music.repeat}
                    on:click={appState.music.toggleRepeat}>
                <Fa icon={faRepeat}/>
            </button>
        </div>

        <div class="flex place-items-center gap-6">
            <span>{minutesToTime($appState.music.position)}</span>
            <ProgressBar max={1} value={$appState.music.position / appState.music.currentItem().duration}/>
            <span>{minutesToTime(appState.music.currentItem().duration)}</span>
        </div>
    </div>

    <div class="flex place-items-center place-content-end gap-4 mr-10">
        <button class="btn-icon variant-ghost" on:click={() => weckpiCore.action("music.stop")}>
            <Fa icon={faStop}/>
        </button>

        <button class="btn-icon variant-ghost" on:click={onVolumeButtonClick} use:popup={volumePopupSettings}>
            <Fa icon={volumeIcon($appState.music.volume)}/>
        </button>
    </div>

    <div class="p-4 bg-surface-400-500-token rounded-lg" data-popup="volumePopup">
        <input class="h-20" id="volumeSlider" max="100" on:change={onVolumeSliderChange} orient="vertical"
               type="range" value={$appState.music.volume}/>
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
