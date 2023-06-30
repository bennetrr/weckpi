import type {WeckPiCoreConnection} from "$lib/BackendConnection/WeckPiCoreConnection";
import {musicMetadata, musicPlaying, musicRepeat, musicShuffle, musicVolume, musicPosition} from "$lib/BackendConnection/ParameterStore";
import {weckpiCore} from "$lib/BackendConnection/WeckPiCoreConnection";

export function initializeWeckPiCoreCommunication(weckPiCore: WeckPiCoreConnection) {
    // Request the initial dataset
    weckPiCore.getInitialData((initialData) => {
        musicMetadata.set(initialData.music.metadata);
        musicPlaying.set(initialData.music.playing);
        musicRepeat.set(initialData.music.repeat);
        musicShuffle.set(initialData.music.shuffle);
        musicVolume.set(initialData.music.volume);
        musicPosition.set(initialData.music.position);

        weckpiCore.update(x => {x.enable(); return x});
    })

    // Set the handler for incoming messages
    weckPiCore.onPropertyChange((prop, value) => {
        console.log(`Received property change of ${prop} to ${value} from WeckPi Core`);

        switch (prop) {
            case "music.metadata":
                musicMetadata.set(value);
                break

            case "music.is_playing":
                musicPlaying.set(value);
                break

            case "music.repeat":
                musicRepeat.set(value);
                break

            case "music.shuffle":
                musicShuffle.set(value);
                break

            case "music.volume":
                musicVolume.set(value);
                break

            case "music.position":
                musicPosition.set(value);
                break
        }
    });

    // Set the handlers for outgoing messages (changes in stores)
    musicPlaying.subscribe((value) => weckPiCore.propertyChange("music.is_playing", value));
    musicRepeat.subscribe((value) => weckPiCore.propertyChange("music.repeat", value));
    musicShuffle.subscribe((value) => weckPiCore.propertyChange("music.shuffle", value));
    musicVolume.subscribe((value) => weckPiCore.propertyChange("music.volume", value));
    musicPosition.subscribe((value) => weckPiCore.propertyChange("music.position", value));

    // TODO Handlers for error and close
}
