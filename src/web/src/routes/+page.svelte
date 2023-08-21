<script lang="ts">
    import {AppBar, AppShell} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faCog} from "@fortawesome/free-solid-svg-icons";

    import Clock from "$lib/components/Clock.svelte";
    import MusicControl from "$lib/components/music/MusicControl.svelte";
    import MusicQueue from "$lib/components/music/MusicQueue.svelte";
</script>

<svelte:head>
    <title>WeckPi</title>
</svelte:head>

<AppShell class="select-none">
    <svelte:fragment slot="header">
        <AppBar slotTrail="place-content-end">
            <span>WeckPi</span>

            <svelte:fragment slot="trail">
                <a href="/settings/" title="Einstellungen öffnen">
                    <Fa icon={faCog}/>
                </a>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <svelte:fragment slot="sidebarLeft">
        <MusicQueue/>
    </svelte:fragment>

    <main class="flex place-items-center place-content-center h-full">
        <Clock/>
    </main>

    <svelte:fragment slot="footer">
        <MusicControl/>
    </svelte:fragment>
</AppShell>
