<script lang="ts">
    import Fa from "svelte-fa/src/fa.svelte";
    import {faCog} from "@fortawesome/free-solid-svg-icons";

    import {AppBar, AppShell} from "@skeletonlabs/skeleton";

    import MusicControl from "./MusicControl.svelte";
    import Clock from "./Clock.svelte";
    import MusicQueue from "./MusicQueue.svelte";
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

    <svelte:fragment slot="sidebarLeft">
        <MusicQueue/>
    </svelte:fragment>

    <main class="flex place-items-center place-content-center h-full h1">
        <Clock/>
    </main>

    <svelte:fragment slot="footer">
        <MusicControl/>
    </svelte:fragment>
</AppShell>
