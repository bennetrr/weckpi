<script lang="ts">
    import {musicMetadata, musicPosition} from "$lib/stores/ContentStore";

    //@ts-ignore
    import Fa from "svelte-fa";
    import {faCog} from "@fortawesome/free-solid-svg-icons";

    import {AppBar, AppShell} from "@skeletonlabs/skeleton";

    import MusicControl from "./MusicControl.svelte";
    import {onMount} from "svelte";

    $musicMetadata = {
        title: "Beloved",
        artist: "VNV Nation",
        album: "Futureperfect",
        image_uri: "https://resources.tidal.com/images/2a85ef7a/1aef/43cc/8d2f/e9911c757c1a/1280x1280.jpg",
        duration: 7 + 24 / 60
    }

    $musicPosition = 0.47

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

<svelte:head>
    <title>WeckPi</title>
</svelte:head>

<AppShell>
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

    <main class="flex place-items-center place-content-center h-full h1 ">
        <span class="w-60">{hour} : {minutes} : {seconds}</span>
    </main>

    <svelte:fragment slot="footer">
        <MusicControl/>
    </svelte:fragment>
</AppShell>
