import {writable} from "svelte/store";

interface MusicMetadata {
    title: string;
    artist: string;
    album: string;
    image_uri: string;
    duration: number;
}

export const musicMetadata = writable<MusicMetadata>();
export const musicPosition = writable<number>();
export const musicPlaying = writable<boolean>();
export const musicShuffle = writable<boolean>();
export const musicRepeat = writable<boolean>();
export const musicVolume = writable<number>();