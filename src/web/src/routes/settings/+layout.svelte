<script>
    import {faArrowLeft} from "@fortawesome/free-solid-svg-icons";
    import {AppBar, AppShell} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa";
</script>

<AppShell>
    <svelte:fragment slot="header">
        <AppBar slotTrail="place-content-end">
            <span>WeckPi Settings</span>

            <svelte:fragment slot="trail">
                <a href="/" title="Bo back">
                    <Fa icon={faArrowLeft}/>
                </a>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>

    <svelte:fragment slot="sidebarLeft">
        Settings Navigation
    </svelte:fragment>
</AppShell>

