<script>
    // Skeleton
    import "@skeletonlabs/skeleton/themes/theme-crimson.css";
    import "@skeletonlabs/skeleton/styles/skeleton.css";
    import "../app.postcss";
    import {arrow, autoUpdate, computePosition, flip, offset, shift} from "@floating-ui/dom";
    import {storePopup} from "@skeletonlabs/skeleton";

    storePopup.set({computePosition, autoUpdate, offset, shift, flip, arrow});
</script>

<slot />
