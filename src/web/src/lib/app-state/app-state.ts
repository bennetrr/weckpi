import {onSnapshot, types} from "mobx-state-tree";

import {Music} from "$lib/app-state/music-store";

const AppState = types.model("AppState", {
    music: Music,
    initialized: types.boolean
}).actions(self => ({
    subscribe(method: any) {
        method(self);
        return onSnapshot(appState, method);
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
    initialized: false
});

onSnapshot(appState, console.log);

export default appState;
