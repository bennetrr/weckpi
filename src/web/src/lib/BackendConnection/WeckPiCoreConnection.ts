import {io, type Socket} from "socket.io-client";

import {musicMetadata, musicPlaying, musicPosition, musicRepeat, musicShuffle, musicVolume} from "$lib/BackendConnection/ParameterStore";

import {debug} from "debug";

const log = debug("weckpiWeb:weckpiCoreConnection");

export class WeckPiCoreConnection {
    public sio: Socket;
    private disabled: boolean;

    public constructor() {
        log("Initializing weckpi core connection");
        this.sio = io("ws://localhost:8000/");
        this.disabled = true;

        // Set the handler for incoming messages
        this.sio.on("property-change", ({prop, value}) => {
            this.disable();
            log("Received property change of %s to %O", prop, value);
            console.error("Received property change of %s to %O", prop, value)

            switch (prop) {
                case "music.metadata":
                    musicMetadata.set(value);
                    break;

                case "music.is_playing":
                    musicPlaying.set(value);
                    break;

                case "music.repeat":
                    musicRepeat.set(value);
                    break;

                case "music.shuffle":
                    musicShuffle.set(value);
                    break;

                case "music.volume":
                    musicVolume.set(value);
                    break;

                case "music.position":
                    musicPosition.set(value);
                    break;
            }

            this.enable();
        });

        // Set the handlers for outgoing messages (changes in stores)
        musicPlaying.subscribe((value) => this.propertyChange("music.is_playing", value));
        musicRepeat.subscribe((value) => this.propertyChange("music.repeat", value));
        musicShuffle.subscribe((value) => this.propertyChange("music.shuffle", value));
        musicVolume.subscribe((value) => this.propertyChange("music.volume", value));
        musicPosition.subscribe((value) => this.propertyChange("music.position", value));

        // Request the initial dataset
        this.sio.emit("initial-data-request", (initialData: any) => {
            musicMetadata.set(initialData.music.metadata);
            musicPlaying.set(initialData.music.playing);
            musicRepeat.set(initialData.music.repeat);
            musicShuffle.set(initialData.music.shuffle);
            musicVolume.set(initialData.music.volume);
            musicPosition.set(initialData.music.position);

            this.enable();
        });

        this.sio.prependAny((name, data) => log("Received event %s with data %O", name, data));
    }

    public enable() {
        log("Enabled sending of events");
        this.disabled = false;
    }

    public disable() {
        log("Disabled sending of events");
        this.disabled = true;
    }

    public propertyChange(prop: string, value: any) {
        if (this.disabled) {
            log("Change of property %s suppressed, because disabled=%s", prop, this.disabled);
            return;
        }

        log("Sent change of property %s to value %O", prop, value);
        this.sio.emit("property-change", {prop, value});
    }

    public action(name: string) {
        if (this.disabled) {
            log("Action %s suppressed, because disabled=%s", name, this.disabled);
            return;
        }

        log("Sent action %s", name);
        this.sio.emit("action", {name});
    }
}


const weckpiCore: WeckPiCoreConnection = new WeckPiCoreConnection();
export default weckpiCore;
