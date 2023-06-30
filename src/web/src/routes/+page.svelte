<script lang="ts">
    //@ts-ignore
    import Fa from "svelte-fa";
    import {faCog} from "@fortawesome/free-solid-svg-icons";

    import {musicMetadata, musicPlaying, musicPosition, musicRepeat, musicShuffle, musicVolume} from "$lib/BackendConnection/ParameterStore";

    import {onMount} from "svelte";
    import {AppBar, AppShell} from "@skeletonlabs/skeleton";

    import MusicControl from "./MusicControl.svelte";
    import Clock from "./Clock.svelte";
    import {WeckPiCoreConnection, weckpiCore} from "$lib/BackendConnection/WeckPiCoreConnection";
    import {initializeWeckPiCoreCommunication} from "$lib/BackendConnection/ParameterCommunication";

    onMount(() => {
        $weckpiCore = new WeckPiCoreConnection();
        initializeWeckPiCoreCommunication($weckpiCore);
    });
</script>

<svelte:head>
    <title>WeckPi</title>
</svelte:head>

<AppShell class="select-none">
    <svelte:fragment slot="header">
        <AppBar slotTrail="place-content-end">
            <span>WeckPi</span>

            <svelte:fragment slot="trail">
                <a href="/settings" title="Open Settings">
                    <Fa icon={faCog}/>
                </a>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <main class="flex place-items-center place-content-center h-full h1">
        <Clock/>
    </main>

    <svelte:fragment slot="footer">
        <MusicControl/>
    </svelte:fragment>
</AppShell>
