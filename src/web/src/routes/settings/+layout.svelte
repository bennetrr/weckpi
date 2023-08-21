<script lang="ts">
    import {debug} from "debug";

    import {AppBar, AppShell} from "@skeletonlabs/skeleton";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faArrowLeft, faBell, faMusic} from "@fortawesome/free-solid-svg-icons";

    import SidenavItem from "$lib/components/SidenavItem.svelte";

    const log = debug("weckPiWeb:layout:/settings/");
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
        <div class="flex flex-col w-[250px] h-full bg-surface-200-700-token">
            <SidenavItem icon={faBell} name="Wecker" path="/settings/alarm/"/>
            <SidenavItem icon={faMusic} name="Musik" path="/settings/music/"/>
        </div>
    </svelte:fragment>

    <div class="p-4">
        <slot/>
    </div>
</AppShell>
