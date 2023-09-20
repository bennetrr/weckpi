import {debug} from "debug";
import {io, type Socket} from "socket.io-client";
import {applyPatch, applySnapshot, type IJsonPatch, onPatch} from "mobx-state-tree";

import {PUBLIC_WECKPI_CORE_URL} from "$env/static/public";
import appState from "$lib/app-state/app-state";

const log = debug("weckPiWeb:backend");

export class BackendConnection {
    public sio: Socket;
    private disabled: boolean;

    public constructor() {
        log("Initializing connection to the WeckPi backend on %s", PUBLIC_WECKPI_CORE_URL);
        this.sio = io(PUBLIC_WECKPI_CORE_URL);
        this.disabled = true;

        // Set the handler for incoming patches
        this.sio.on("appStatePatch", ({prop: path, value}) => {
            this.disable();  // TODO Better blocking system than disabling and enabling
            log("Incoming patch: %s to %o", path, value);
            applyPatch(appState, {path, value, op: "replace"});  // TODO Use JSONPatch in the backend
            this.enable();
        });

        // Set the handler for outgoing patches
        onPatch(appState, patch => this.sendAppStatePatch(patch));

        // Request the initial app state
        this.sio.emit("initialAppState", (snapshot: any) => {
            log("Received initial app state: %O", snapshot);
            applySnapshot(appState, snapshot);
            this.enable();
        });

        this.sio.prependAny((name, data) => log("Received event %s with data %o", name, data));
    }

    public enable() {
        log("Enabled sending of events");
        this.disabled = false;
    }

    public disable() {
        log("Disabled sending of events");
        this.disabled = true;
    }

    public sendAppStatePatch({path, value}: IJsonPatch) {
        log("%O", this)
        if (this.disabled) {
            log("Outgoing patch suppressed (disabled=%s): %s to %o", this.disabled, path, value);
            return;
        }

        log("Outgoing patch: %s to %o", path, value);
        this.sio.emit("appStatePatch", {path, value});  // TODO Use JSONPatch in the backend
    }

    public sendAction(name: string) {
        if (this.disabled) {
            log("Outgoing action suppressed (disabled=%s): %s", this.disabled, name);
            return;
        }

        log("Outgoing action: %s", name);
        this.sio.emit("action", {name});
    }
}

const backend: BackendConnection = new BackendConnection();
export default backend;
