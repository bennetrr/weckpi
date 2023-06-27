<script lang="ts">
    //@ts-ignore
    import Fa from "svelte-fa";
    import {faCog} from "@fortawesome/free-solid-svg-icons";

    import {musicMetadata, musicPlaying, musicPosition, musicRepeat, musicShuffle, musicVolume} from "$lib/BackendConnection/ParameterStore";

    import {onMount, setContext} from "svelte";
    import {AppBar, AppShell} from "@skeletonlabs/skeleton";

    import MusicControl from "./MusicControl.svelte";
    import Clock from "./Clock.svelte";

    $musicMetadata = {
            title: "Beloved",
            artist: "VNV Nation",
            album: "Futureperfect",
            image_uri: "https://resources.tidal.com/images/2a85ef7a/1aef/43cc/8d2f/e9911c757c1a/1280x1280.jpg",
            duration: 7 + 24 / 60
        };

        $musicPosition = 1.20;
        $musicPlaying = true;
        $musicShuffle = true;
        $musicRepeat = false;
        $musicVolume = 50;

    onMount(() => {
        const weckPiCoreConnection = new WebSocket("ws://localhost:8080");
        setContext("weckPiCoreConnection", weckPiCoreConnection);




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
