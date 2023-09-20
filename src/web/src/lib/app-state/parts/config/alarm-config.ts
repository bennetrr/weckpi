import {debug} from "debug";
import {getSnapshot, type Instance, types} from "mobx-state-tree";
import {DateTime} from "luxon";

const log = debug("weckPiWeb:appState:config:alarm");

/** The ISO-8601 weekday number, where 1 is Monday and 7 is Sunday. */
type IsoWeekday = 1 | 2 | 3 | 4 | 5 | 6 | 7;

/** Custom MST type for luxon's DateTime object that serializes to the ISO-8601 time format. */
const Time = types.custom<string, DateTime>({
    name: "Time",
    fromSnapshot(snapshot: string): DateTime {
        return DateTime.fromISO(snapshot);
    },
    toSnapshot(value: DateTime): string {
        return value.toISOTime({includeOffset: false})!;
    },
    isTargetType(value: DateTime | string): boolean {
        return value instanceof DateTime;
    },
    getValidationMessage(snapshot: string): string {
        const dt = DateTime.fromISO(snapshot);
        return dt.isValid ? "" : dt.invalidExplanation!;
    }
});

const AlarmDay = types.model({
    active: types.boolean,
    time: Time,
    overrideActive: types.boolean,
    overrideTime: Time
});

export const AlarmConfig = types.model({
    monday: AlarmDay,
    tuesday: AlarmDay,
    wednesday: AlarmDay,
    thursday: AlarmDay,
    friday: AlarmDay,
    saturday: AlarmDay,
    sunday: AlarmDay
}).views(self => ({
    getAlarmConfig(weekday: IsoWeekday) {
        switch (weekday) {
            case 1:
                return self.monday;
            case 2:
                return self.tuesday;
            case 3:
                return self.wednesday;
            case 4:
                return self.thursday;
            case 5:
                return self.friday;
            case 6:
                return self.saturday;
            case 7:
                return self.sunday;
            default:
                throw new Error("Invalid weekday");
        }
    }
})).views(self => ({
    /** Get the alarm that would go off next. */
    getNextAlarm() {
        // Get a list of all weekdays beginning with the current weekday
        const currentTime = DateTime.local().set({
            day: self.getAlarmConfig(1).time.day,
            year: self.getAlarmConfig(1).time.year,
            month: self.getAlarmConfig(1).time.month
        });
        const currentWeekday = (DateTime.local().weekday as IsoWeekday);

        const weekdays = ([1, 2, 3, 4, 5, 6, 7]
            .slice(currentWeekday - 1)
            .concat([1, 2, 3, 4, 5, 6, 7]
                .slice(0, currentWeekday - 1)) as IsoWeekday[]);

        log("currentTime=%s, currentWeekday=%s, weekdays=%o", currentTime, currentWeekday, weekdays);

        // Find the first weekday with an active alarm
        for (const weekday of weekdays) {
            const alarmConfig: Instance<typeof AlarmDay> = self.getAlarmConfig(weekday);
            log("weekday=%s, alarmConfig=%o", weekday, getSnapshot(alarmConfig));

            // Check if the alarm is active and, if it's today's alarm, check if the alarm is still in the future
            if (alarmConfig.overrideActive && (weekday !== currentWeekday || alarmConfig.overrideTime > currentTime)) {
                return {time: alarmConfig.overrideTime, weekday: weekday};
            }

            // Same for the normal alarm time
            if (alarmConfig.active && (weekday !== currentWeekday || alarmConfig.time > currentTime)) {
                return {time: alarmConfig.time, weekday: weekday};
            }
        }

        return null;
    }
})).actions(self => ({
    setActive(weekday: IsoWeekday, value: boolean) {
        self.getAlarmConfig(weekday).active = value;
    },
    setTime(weekday: IsoWeekday, value: DateTime) {
        self.getAlarmConfig(weekday).time = value;
    },
    setOverrideActive(weekday: IsoWeekday, value: boolean) {
        self.getAlarmConfig(weekday).overrideActive = value;
    },
    setOverrideTime(weekday: IsoWeekday, value: DateTime) {
        self.getAlarmConfig(weekday).overrideTime = value;
    }
}));
