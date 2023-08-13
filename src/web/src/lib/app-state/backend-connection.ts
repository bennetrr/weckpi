import {io, type Socket} from "socket.io-client";
import {debug} from "debug";
//@ts-ignore
import {PUBLIC_WECKPI_CORE_URL} from "$env/static/public";

import appState from "$lib/app-state/app-state";
import {applyPatch, applySnapshot, onPatch} from "mobx-state-tree";

const log = debug("weckpiWeb:weckpiCoreConnection");

export class WeckPiCoreConnection {
    public sio: Socket;
    private disabled: boolean;

    public constructor() {
        log("Initializing connection to weckpi core on %s", PUBLIC_WECKPI_CORE_URL);
        this.sio = io(PUBLIC_WECKPI_CORE_URL);
        this.disabled = true;

        // Set the handler for incoming patches
        this.sio.on("appStatePatch", ({prop, value}) => {
            this.disable();
            log("Received app state patch of %s to %O", prop, value);
            applyPatch(appState, {path: prop, value: value, op: "replace"});
            this.enable();
        });

        // Set the handler for outgoing patches
        onPatch(appState, patch => {
            this.propertyChange(patch.path, patch.value);
        });

        // Request the initial app state
        this.sio.emit("initialAppState", (snapshot: any) => {
            log("Received initial dataset: %O", snapshot);
            applySnapshot(appState, snapshot);
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

    public propertyChange<T>(prop: string, value: T) {
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
