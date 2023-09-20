<script lang="ts">
    import {debug} from "debug";
    import {page} from "$app/stores";

    import Fa from "svelte-fa/src/fa.svelte";
    import {type IconDefinition} from "@fortawesome/free-solid-svg-icons";

    const log = debug("weckPiWeb:ui:sidenavItem");

    export let name: string;
    export let icon: IconDefinition;
    export let path: string;
</script>

<a aria-current={$page.url.pathname === path} class="sidenav-item" href={path}>
    <Fa icon={icon}/>
    <span>{name}</span>
</a>

<style lang="postcss">
    .sidenav-item {
        @apply p-4 flex gap-2 place-items-center hover:bg-surface-800-100-token
    }

    .sidenav-item[aria-current="true"] {
        @apply border-l-8 border-primary-700 pl-2
    }
</style>
