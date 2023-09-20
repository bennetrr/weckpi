import {debug} from "debug";
import {Duration} from "luxon";

const log = debug("weckPiWeb:utils:dateTime");

/** Convert the given amount of minutes into a human-readable time format ([HH:][M]M:SS) */
export function minutesToTime(minutes: number, showZeroHours = false): string {
    const duration = Duration.fromObject({minute: minutes});

    if (showZeroHours || duration.hours > 0) {
        return duration.toFormat("H:mm:ss");
    }

    return duration.toFormat("m:ss");
}
