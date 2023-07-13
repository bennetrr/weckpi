import {writable} from "svelte/store";

interface MusicMetadata {
    title: string;
    artist: string;
    album: string;
    image: string;
    duration: number;
}

export const musicQueue = writable<MusicMetadata[]>();
export const musicQueuePosition = writable<number>();
export const musicPosition = writable<number>();
export const musicPlaying = writable<boolean>();
export const musicShuffle = writable<boolean>();
export const musicRepeat = writable<boolean>();
export const musicVolume = writable<number>();
