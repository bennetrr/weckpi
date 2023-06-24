import WeckPiCoreConnection, {type MessageData} from "$lib/BackendConnection/WeckPiCoreConnection";
import {musicMetadata, musicPlaying, musicRepeat, musicShuffle, musicVolume, musicPosition} from "$lib/BackendConnection/ParameterStore";

export function initializeWeckPiCoreCommunication(url: string) {
    // Start the connection
    const weckPiCoreConnection = new WeckPiCoreConnection(url);

    // Set the handler for incoming messages
    weckPiCoreConnection.setOnMessage((messageEvent) => {
        const {propertyName, value}: MessageData = JSON.parse(messageEvent.data);
        console.log(`Received property change of ${propertyName} to ${value} from WeckPi Core`);

        // TODO Initialize the stores with the values from the server

        switch (propertyName) {
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
    musicPlaying.subscribe((value) => weckPiCoreConnection.send({propertyName: "music.is_playing", value}));
    musicRepeat.subscribe((value) => weckPiCoreConnection.send({propertyName: "music.repeat", value}));
    musicShuffle.subscribe((value) => weckPiCoreConnection.send({propertyName: "music.shuffle", value}));
    musicVolume.subscribe((value) => weckPiCoreConnection.send({propertyName: "music.volume", value}));
    musicPosition.subscribe((value) => weckPiCoreConnection.send({propertyName: "music.position", value}));

    // TODO Handlers for error and close

    // Return the connection object
    return weckPiCoreConnection;
}
