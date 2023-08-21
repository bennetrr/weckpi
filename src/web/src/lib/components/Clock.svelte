<script lang="ts">
    import {debug} from "debug";
    import {DateTime} from "luxon";

    import {onMount} from "svelte";
    import Fa from "svelte-fa/src/fa.svelte";
    import {faBell} from "@fortawesome/free-solid-svg-icons";

    import appState from "$lib/app-state/app-state";

    const log = debug("weckPiWeb:ui:clock");

    let dateTime = DateTime.local();
    $: time = dateTime.toFormat("HH:mm:ss");

    onMount(() => {
        const interval = setInterval(() => {
            dateTime = DateTime.local();
        }, 100);

        return () => clearInterval(interval);
    });

    const nextAlarm = $appState.config.alarm.getNextAlarm();
    const nextAlarmText = nextAlarm ? `${["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][nextAlarm?.weekday - 1]}, ${nextAlarm.time.toFormat("HH:mm")}` : null;
</script>

<div class="flex flex-col place-items-center">
    <span class="h1">{time}</span>

    {#if nextAlarmText}
        <div class="flex gap-2 place-items-center">
            <Fa icon={faBell}/>
            <span>{nextAlarmText}</span>
        </div>
    {/if}
</div>
