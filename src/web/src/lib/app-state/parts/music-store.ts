import {debug} from "debug";
import {types} from "mobx-state-tree";

const log = debug("weckPiWeb:appState:music");

const Queue = types.model({
    title: types.string,
    artist: types.string,
    album: types.string,
    image: types.optional(types.string, "/song.svg"),
    duration: types.number
});

export const Music = types.model({
    queue: types.array(Queue),
    queuePosition: types.number,
    position: types.number,
    isPlaying: types.boolean,
    shuffle: types.boolean,
    repeat: types.boolean,
    volume: types.number
}).actions(self => ({
    toggleIsPlaying() {
        self.isPlaying = !self.isPlaying;
    },
    toggleShuffle() {
        self.shuffle = !self.shuffle;
    },
    toggleRepeat() {
        self.repeat = !self.repeat;
    },
    setQueuePosition(value: number) {
        self.queuePosition = value;
    },
    setPosition(value: number) {
        self.position = value;
    },
    setVolume(value: number) {
        self.volume = value;
    }
})).views(self => ({
    currentItem() {
        return self.queue[self.queuePosition];
    }
}));
