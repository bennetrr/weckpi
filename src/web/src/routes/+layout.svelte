<script>
    import "@skeletonlabs/skeleton/themes/theme-crimson.css";
    import "@skeletonlabs/skeleton/styles/skeleton.css";
    import "../app.postcss";

    import {arrow, autoUpdate, computePosition, flip, offset, shift} from "@floating-ui/dom";
    import {ProgressRadial, storePopup} from "@skeletonlabs/skeleton";
    import appState from "$lib/app-state/app-state";
    import backend from "$lib/app-state/backend-connection";  // Don't delete, this is needed to initialize the connection

    storePopup.set({computePosition, autoUpdate, offset, shift, flip, arrow});
</script>

{#if $appState.initialized}
    <slot/>
{:else}
    <main class="flex place-items-center place-content-center h-full bg-surface-50-900-token">
        <ProgressRadial/>
    </main>
{/if}
