import {io, type Socket} from "socket.io-client";
import {debug} from "debug";
import {PUBLIC_WECKPI_CORE_URL} from "$env/static/public";

import {musicPlaying, musicPosition, musicQueue, musicQueuePosition, musicRepeat, musicShuffle, musicVolume} from "$lib/BackendConnection/ParameterStore";

const log = debug("weckpiWeb:weckpiCoreConnection");

export class WeckPiCoreConnection {
    public sio: Socket;
    private disabled: boolean;

    public constructor() {
        log("Initializing connection to weckpi core on %s", PUBLIC_WECKPI_CORE_URL);
        this.sio = io(PUBLIC_WECKPI_CORE_URL);
        this.disabled = true;

        // Set the handler for incoming messages
        this.sio.on("propertyChange", ({prop, value}) => {
            this.disable();
            log("Received property change of %s to %O", prop, value);

            switch (prop) {
                case "music.queue":
                    musicQueue.set(value);
                    break;

                case "music.queuePosition":
                    musicQueuePosition.set(value);
                    break;

                case "music.isPlaying":
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
        musicQueue.subscribe((value) => this.propertyChange("music.queue", value));
        musicQueuePosition.subscribe((value) => this.propertyChange("music.queuePosition", value));
        musicPlaying.subscribe((value) => this.propertyChange("music.isPlaying", value));
        musicRepeat.subscribe((value) => this.propertyChange("music.repeat", value));
        musicShuffle.subscribe((value) => this.propertyChange("music.shuffle", value));
        musicVolume.subscribe((value) => this.propertyChange("music.volume", value));
        musicPosition.subscribe((value) => this.propertyChange("music.position", value));

        // Request the initial dataset
        this.sio.emit("initialDataRequest", (initialData: any) => {
            log("Received initial dataset: %O", initialData)
            musicQueue.set(initialData.music.queue);
            musicQueuePosition.set(initialData.music.queuePosition);
            musicPlaying.set(initialData.music.isPlaying);
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
        this.sio.emit("propertyChange", {prop, value});
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
