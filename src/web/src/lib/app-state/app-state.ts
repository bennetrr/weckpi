import {debug} from "debug";
import {onPatch, onSnapshot, types} from "mobx-state-tree";

import {Music} from "$lib/app-state/parts/music-store";
import {Config} from "$lib/app-state/parts/config/root-config";

const log = debug("weckpiWeb:appState");

const AppState = types.model("AppState", {
    music: Music,
    initialized: types.boolean,
    config: Config
}).actions(self => ({
    subscribe(method: any) {
        method(self);
        return onSnapshot(appState, () => method(self));
    }
}));

const appState = AppState.create({
    music: {
        queue: [],
        queuePosition: 0,
        position: 0,
        isPlaying: false,
        shuffle: false,
        repeat: false,
        volume: 100
    },
    initialized: false,
    config: {
        alarm: {
            monday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            tuesday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            wednesday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            thursday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            friday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            saturday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            },
            sunday: {
                active: true,
                time: "08:00:00",
                overrideActive: false,
                overrideTime: "09:00:00"
            }
        }
    }
});

onPatch(appState, patch => log("New %s patch: %s to %o", patch.op, patch.path, patch.value));
onSnapshot(appState, snapshot => log("New snapshot: %o", snapshot));

export default appState;
