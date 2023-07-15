import {writable} from "svelte/store";

export interface MusicMetadata {
    title: string;
    artist: string;
    album: string;
    image: string;
    duration: number;
}

export const musicQueue = writable<MusicMetadata[]>([{
    image: "", artist: "", album: "", title: "", duration: 0
}]);
export const musicQueuePosition = writable<number>(0);
export const musicPosition = writable<number>();
export const musicPlaying = writable<boolean>();
export const musicShuffle = writable<boolean>();
export const musicRepeat = writable<boolean>();
export const musicVolume = writable<number>();
