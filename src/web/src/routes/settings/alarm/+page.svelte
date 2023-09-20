<script lang="ts">
    import {debug} from "debug";
    import {DateTime} from "luxon";

    import appState from "$lib/app-state/app-state";

    const log = debug("weckPiWeb:page:/settings/alarm");

    function onActiveChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const weekday = parseInt(target.dataset.weekday);
        log("Active changed: weekday=%s, active=%s", weekday, target.checked);

        appState.config.alarm.setActive(weekday, target.checked);
    }

    function onTimeChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const weekday = parseInt(target.dataset.weekday);
        log("Time changed: weekday=%s, time=%s", weekday, target.value);

        appState.config.alarm.setTime(weekday, DateTime.fromFormat(target.value, "HH:mm"));
    }

    function onOverrideActiveChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const weekday = parseInt(target.dataset.weekday);
        log("Override active changed: weekday=%s, active=%s", weekday, target.checked);

        appState.config.alarm.setOverrideActive(weekday, target.checked);
    }

    function onOverrideTimeChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const weekday = parseInt(target.dataset.weekday);
        log("Override time changed: weekday=%s, time=%s", weekday, target.value);

        appState.config.alarm.setOverrideTime(weekday, DateTime.fromFormat(target.value, "HH:mm"));
    }
</script>

<div class="table-container">
    <table class="table table-hover">
        <thead>
        <tr>
            <th>Tag</th>
            <th>Aktiviert</th>
            <th>Zeit</th>
            <th>Überschreiben</th>
            <th>Überschriebene Zeit</th>
        </tr>
        </thead>
        <tbody>
        {#each [1, 2, 3, 4, 5, 6, 7] as weekday}
            <tr>
                <td>
                    {["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"][weekday - 1]}
                </td>
                <td>
                    <input data-weekday={weekday} class="checkbox" type="checkbox"
                           checked={$appState.config.alarm.getAlarmConfig(weekday).active} on:click={onActiveChange}/>
                </td>
                <td>
                    <input data-weekday={weekday} class="input" type="time"
                           value={$appState.config.alarm.getAlarmConfig(weekday).time.toFormat("HH:mm")}
                           on:change={onTimeChange}/>
                </td>
                <td>
                    <input data-weekday={weekday} class="checkbox" type="checkbox"
                           checked={$appState.config.alarm.getAlarmConfig(weekday).overrideActive}
                           on:click={onOverrideActiveChange}/>
                </td>
                <td>
                    <input data-weekday={weekday} class="input" type="time"
                           value={$appState.config.alarm.getAlarmConfig(weekday).overrideTime.toFormat("HH:mm")}
                           on:change={onOverrideTimeChange}/>
                </td>
            </tr>
        {/each}
        </tbody>
    </table>
</div>
