/**
 * Convert the given amount of minutes into a human-readable time format ([HH:][M]M:SS)
 */
export function minutesToTime(minutes: number, showZeroHours: boolean = false): string {
    const hours = Math.floor(minutes / 60);
    const minutesLeft = Math.floor(minutes % 60);
    const seconds = Math.floor((minutes - Math.floor(minutes)) * 60);

    let time = `${minutesLeft}:${seconds.toString().padStart(2, "0")}`;
    if (hours > 0 || showZeroHours) {
        time = `${hours}:${time}`;
    }

    console.log(`Converted ${minutes} minutes to ${time}`);

    return time;
}
